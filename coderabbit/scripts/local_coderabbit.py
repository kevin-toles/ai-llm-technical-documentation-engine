#!/usr/bin/env python3
"""
Local CodeRabbit Analysis Runner
Provides local code analysis capabilities similar to CodeRabbit's GitHub integration
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class LocalCodeRabbitAnalyzer:
    def __init__(self, config_path: str = ".coderabbit.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.results = []
        
    def load_config(self) -> Dict[str, Any]:
        """Load CodeRabbit configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Configuration file {self.config_path} not found")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if file not found"""
        return {
            "analysis": {
                "enabled": True,
                "mode": "standard",
                "scope": {
                    "include_patterns": ["**/*.py"],
                    "exclude_patterns": ["__pycache__/**", ".git/**"]
                }
            }
        }
    
    def run_security_analysis(self) -> List[Dict]:
        """Run security analysis using bandit"""
        print("🔒 Running security analysis...")
        
        try:
            result = subprocess.run([
                'bandit', '-r', '.', 
                '-f', 'json',
                '--exclude', '__pycache__,.git,venv,env,.pytest_cache,.mypy_cache,docker_volumes,cache_storage,logs,backups',
                '--quiet'  # Suppress warnings
            ], capture_output=True, text=True)
            
            if result.stdout.strip():
                try:
                    bandit_data = json.loads(result.stdout)
                    security_issues = []
                    
                    for issue in bandit_data.get('results', []):
                        security_issues.append({
                            'tool': 'bandit',
                            'type': 'security',
                            'severity': issue.get('issue_severity', 'medium').lower(),
                            'file': issue.get('filename', ''),
                            'line': issue.get('line_number', 1),
                            'message': issue.get('issue_text', ''),
                            'rule': issue.get('test_id', ''),
                            'confidence': issue.get('issue_confidence', 'unknown')
                        })
                    
                    return security_issues
                except json.JSONDecodeError:
                    print("⚠️  Bandit output parsing failed")
                    return []
            else:
                print("✅ No security issues found")
                return []
                
        except FileNotFoundError:
            print("⚠️  Bandit not installed. Install with: pip install bandit")
            return []
    
    def run_code_quality_analysis(self) -> List[Dict]:
        """Run code quality analysis using flake8 and pylint"""
        print("📊 Running code quality analysis...")
        
        issues = []
        
        # Run flake8
        try:
            result = subprocess.run([
                'flake8', '--format=json', '--exclude=__pycache__,.git,venv,env'
            ], capture_output=True, text=True)
            
            if result.stdout:
                flake8_results = json.loads(result.stdout)
                for issue in flake8_results:
                    issues.append({
                        'tool': 'flake8',
                        'type': 'code_quality',
                        'severity': 'medium',
                        'file': issue['filename'],
                        'line': issue['line_number'],
                        'message': issue['text'],
                        'rule': issue['code']
                    })
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️  Flake8 analysis failed")
        
        # Run ruff (if available)
        try:
            result = subprocess.run([
                'ruff', 'check', '--output-format=json', '.'
            ], capture_output=True, text=True)
            
            if result.stdout:
                ruff_results = json.loads(result.stdout)
                for issue in ruff_results:
                    issues.append({
                        'tool': 'ruff',
                        'type': 'code_quality',
                        'severity': 'medium',
                        'file': issue['filename'],
                        'line': issue['location']['row'],
                        'message': issue['message'],
                        'rule': issue['code']
                    })
        except (FileNotFoundError, json.JSONDecodeError):
            print("ℹ️  Ruff not available")
        
        return issues
    
    def run_complexity_analysis(self) -> List[Dict]:
        """Run complexity analysis using radon"""
        print("🧮 Running complexity analysis...")
        
        try:
            result = subprocess.run([
                'radon', 'cc', '.', '-j', '--exclude=__pycache__,.git,venv,env'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    complexity_data = json.loads(result.stdout)
                    issues = []
                    
                    for file_path, metrics in complexity_data.items():
                        if isinstance(metrics, list):
                            for metric in metrics:
                                if isinstance(metric, dict) and 'complexity' in metric:
                                    complexity_score = metric.get('complexity', 0)
                                    if isinstance(complexity_score, (int, float)) and complexity_score > 10:
                                        issues.append({
                                            'tool': 'radon',
                                            'type': 'complexity',
                                            'severity': 'high' if complexity_score > 15 else 'medium',
                                            'file': file_path,
                                            'line': metric.get('lineno', 1),
                                            'message': f"High complexity: {complexity_score} (threshold: 10)",
                                            'rule': 'complexity',
                                            'complexity': complexity_score
                                        })
                    
                    return issues
                except json.JSONDecodeError:
                    print("⚠️  Radon output parsing failed")
                    return []
                
        except FileNotFoundError:
            print("⚠️  Radon not installed. Install with: pip install radon")
            return []
        
        return []
    
    def run_type_checking(self) -> List[Dict]:
        """Run type checking using mypy"""
        print("🔍 Running type checking...")
        
        try:
            result = subprocess.run([
                'mypy', '.', '--show-error-codes', '--no-error-summary'
            ], capture_output=True, text=True)
            
            issues = []
            for line in result.stdout.split('\n'):
                if line.strip() and ':' in line:
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        issues.append({
                            'tool': 'mypy',
                            'type': 'type_safety',
                            'severity': 'medium',
                            'file': parts[0],
                            'line': int(parts[1]) if parts[1].isdigit() else 1,
                            'message': parts[3].strip(),
                            'rule': 'type-check'
                        })
            
            return issues
            
        except (FileNotFoundError, ValueError):
            print("⚠️  MyPy analysis failed")
            return []
    
    def run_documentation_check(self) -> List[Dict]:
        """Check documentation coverage"""
        print("📚 Checking documentation...")
        
        # This is a simplified check - you could integrate with pydocstyle
        issues = []
        
        for py_file in Path('.').rglob('*.py'):
            if any(exclude in str(py_file) for exclude in ['__pycache__', '.git', 'venv']):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                # Simple check for missing docstrings
                if 'def ' in content and '"""' not in content and "'''" not in content:
                    issues.append({
                        'tool': 'doc-checker',
                        'type': 'documentation',
                        'severity': 'low',
                        'file': str(py_file),
                        'line': 1,
                        'message': 'Missing docstrings in functions/classes',
                        'rule': 'missing-docstring'
                    })
            except Exception:
                continue
                
        return issues
    
    def analyze(self, target_path: str = ".") -> Dict[str, Any]:
        """Run comprehensive code analysis"""
        print(f"🚀 Starting CodeRabbit-style analysis for: {target_path}")
        print(f"📅 Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        os.chdir(target_path)
        
        all_issues = []
        
        # Run different types of analysis
        if self.config.get('analysis', {}).get('rules', {}).get('security', {}).get('enabled', True):
            all_issues.extend(self.run_security_analysis())
        
        if self.config.get('analysis', {}).get('rules', {}).get('code_quality', {}).get('enabled', True):
            all_issues.extend(self.run_code_quality_analysis())
        
        all_issues.extend(self.run_complexity_analysis())
        all_issues.extend(self.run_type_checking())
        
        if self.config.get('analysis', {}).get('rules', {}).get('documentation', {}).get('enabled', True):
            all_issues.extend(self.run_documentation_check())
        
        # Categorize and prioritize issues
        categorized = self.categorize_issues(all_issues)
        
        # Generate summary
        summary = self.generate_summary(categorized)
        
        # Save results
        self.save_results(categorized, summary)
        
        return {
            'summary': summary,
            'issues': categorized,
            'total_issues': len(all_issues)
        }
    
    def categorize_issues(self, issues: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize issues by type and severity"""
        categorized = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }
        
        for issue in issues:
            severity = issue.get('severity', 'medium')
            categorized[severity].append(issue)
        
        return categorized
    
    def generate_summary(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Generate analysis summary"""
        total_issues = sum(len(issues) for issues in categorized.values())
        
        summary = {
            'total_issues': total_issues,
            'by_severity': {
                severity: len(issues) for severity, issues in categorized.items()
            },
            'by_type': {},
            'recommendations': []
        }
        
        # Count by type
        type_counts = {}
        for issues in categorized.values():
            for issue in issues:
                issue_type = issue.get('type', 'unknown')
                type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
        
        summary['by_type'] = type_counts
        
        # Generate recommendations
        if categorized['critical']:
            summary['recommendations'].append("🚨 Address critical security issues immediately")
        
        if categorized['high']:
            summary['recommendations'].append("⚡ Fix high-severity issues before deployment")
        
        if len(categorized['medium']) > 20:
            summary['recommendations'].append("🔧 Consider refactoring to reduce medium-severity issues")
        
        return summary
    
    def save_results(self, categorized: Dict, summary: Dict):
        """Save analysis results to files"""
        # Determine the correct reports directory
        # Script is in coderabbit/scripts/, so reports go in coderabbit/reports/coderabbit/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        coderabbit_dir = os.path.dirname(script_dir)
        reports_dir = os.path.join(coderabbit_dir, 'reports', 'coderabbit')
        
        os.makedirs(reports_dir, exist_ok=True)
        
        # Save JSON report
        json_path = os.path.join(reports_dir, 'analysis_results.json')
        with open(json_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': summary,
                'issues': categorized
            }, f, indent=2)
        
        # Save Markdown report
        self.generate_markdown_report(categorized, summary, reports_dir)
        
        print(f"📊 Results saved to {reports_dir}/")
    
    def generate_markdown_report(self, categorized: Dict, summary: Dict, reports_dir: str):
        """Generate Markdown analysis report"""
        report = []
        report.append("# CodeRabbit Local Analysis Report")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Issues**: {summary['total_issues']}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append("| Severity | Count |")
        report.append("|----------|-------|")
        for severity, count in summary['by_severity'].items():
            emoji = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}.get(severity, '⚪')
            report.append(f"| {emoji} {severity.title()} | {count} |")
        report.append("")
        
        # Recommendations
        if summary['recommendations']:
            report.append("## Recommendations")
            for rec in summary['recommendations']:
                report.append(f"- {rec}")
            report.append("")
        
        # Detailed Issues
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            issues = categorized.get(severity, [])
            if issues:
                emoji = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}.get(severity, '⚪')
                report.append(f"## {emoji} {severity.title()} Issues ({len(issues)})")
                report.append("")
                
                for i, issue in enumerate(issues[:20], 1):  # Limit to first 20
                    report.append(f"### Issue {i}")
                    report.append(f"- **File**: `{issue['file']}`")
                    report.append(f"- **Line**: {issue['line']}")
                    report.append(f"- **Tool**: {issue['tool']}")
                    report.append(f"- **Type**: {issue['type']}")
                    report.append(f"- **Rule**: {issue['rule']}")
                    report.append(f"- **Message**: {issue['message']}")
                    report.append("")
                
                if len(issues) > 20:
                    report.append(f"... and {len(issues) - 20} more issues")
                    report.append("")
        
        md_path = os.path.join(reports_dir, 'analysis_report.md')
        with open(md_path, 'w') as f:
            f.write('\n'.join(report))

def main():
    parser = argparse.ArgumentParser(description='Local CodeRabbit Analysis')
    parser.add_argument('--path', default='.', help='Path to analyze')
    parser.add_argument('--config', default='.coderabbit.json', help='Configuration file')
    parser.add_argument('--format', choices=['json', 'markdown', 'both'], default='both', help='Output format')
    
    args = parser.parse_args()
    
    analyzer = LocalCodeRabbitAnalyzer(args.config)
    results = analyzer.analyze(args.path)
    
    print("\n🎉 Analysis Complete!")
    print(f"📊 Total Issues: {results['total_issues']}")
    print(f"🚨 Critical: {results['summary']['by_severity'].get('critical', 0)}")
    print(f"🔴 High: {results['summary']['by_severity'].get('high', 0)}")
    print(f"🟡 Medium: {results['summary']['by_severity'].get('medium', 0)}")
    print(f"🔵 Low: {results['summary']['by_severity'].get('low', 0)}")

if __name__ == "__main__":
    main()