#!/usr/bin/env python3
"""
CodeRabbit Complete Issues Audit Generator - LLM Document Enhancer
Creates comprehensive audit report from CodeRabbit local analysis results
"""

import json
import os
from datetime import datetime
from collections import defaultdict
from operator import itemgetter

def extract_service_name(file_path):
    """Extract component name from file path"""
    if 'src/phases/' in file_path:
        parts = file_path.split('src/phases/')[1].split('/')
        return f"phases/{parts[0]}" if parts else 'phases'
    elif 'src/' in file_path:
        parts = file_path.split('src/')[1].split('/')
        return f"src/{parts[0]}" if parts else 'src'
    elif 'tests/' in file_path:
        return 'tests'
    elif 'scripts/' in file_path:
        return 'scripts'
    elif 'config/' in file_path:
        return 'config'
    elif 'guidelines/' in file_path:
        return 'guidelines'
    else:
        return 'root'

def get_severity_emoji(severity):
    """Get emoji representation for severity levels"""
    emoji_mapping = {
        'critical': '🚫',
        'high': '🔴', 
        'medium': '🟡',
        'low': '🔵',
        'info': 'ℹ️'
    }
    return emoji_mapping.get(severity, '⚪')

def categorize_issue_type(issue_type):
    """Categorize issue types into readable categories"""
    type_mapping = {
        'security': 'Security Issue',
        'complexity': 'Code Complexity', 
        'code_quality': 'Code Quality',
        'type_safety': 'Type Safety',
        'documentation': 'Documentation'
    }
    return type_mapping.get(issue_type, issue_type.title())

def load_analysis_results():
    """Load and extract issues from CodeRabbit analysis results"""
    # Script is in coderabbit/scripts/, so reports are in coderabbit/reports/coderabbit/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    coderabbit_dir = os.path.dirname(script_dir)
    results_file = os.path.join(coderabbit_dir, "reports", "coderabbit", "analysis_results.json")
    
    if not os.path.exists(results_file):
        print(f"❌ CodeRabbit analysis results not found at: {results_file}")
        return None
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    # Extract all issues from categorized results
    all_issues = []
    for severity, issues in data.get('issues', {}).items():
        for issue in issues:
            issue['severity'] = severity
            all_issues.append(issue)
    
    if not all_issues:
        print("❌ No issues found in results")
        return None
    
    return all_issues

def organize_issues_by_categories(all_issues):
    """Organize issues by service, type, severity, and tool"""
    issues_by_service = defaultdict(list)
    issues_by_type = defaultdict(list)
    issues_by_severity = defaultdict(list)
    issues_by_tool = defaultdict(list)
    
    for issue in all_issues:
        service = extract_service_name(issue.get('file', ''))
        issue_type = issue.get('type', 'unknown')
        severity = issue.get('severity', 'unknown')
        tool = issue.get('tool', 'unknown')
        
        issues_by_service[service].append(issue)
        issues_by_type[issue_type].append(issue)
        issues_by_severity[severity].append(issue)
        issues_by_tool[tool].append(issue)
    
    return issues_by_service, issues_by_type, issues_by_severity, issues_by_tool

def generate_report_header(all_issues):
    """Generate report header section"""
    report = []
    report.append(f"# CodeRabbit_Audit_{datetime.now().strftime('%Y%m%d')}")
    report.append("")
    report.append("**Complete Issue Audit - CodeRabbit Local Analysis**")
    report.append(f"- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("- **Project**: llm-document-enhancer")
    report.append("- **Branch**: main")
    report.append(f"- **Total Issues**: {len(all_issues)}")
    report.append("- **Analysis Tool**: CodeRabbit Local Analyzer")
    report.append("")
    return report

def generate_executive_summary(issues_by_type, issues_by_severity, issues_by_tool, issues_by_service):
    """Generate executive summary section"""
    report = []
    report.append("## Executive Summary")
    report.append("")
    report.append("### Issues by Type")
    for issue_type, issues in sorted(issues_by_type.items(), key=lambda item: len(item[1]), reverse=True):
        category = categorize_issue_type(issue_type)
        count = len(issues)
        report.append(f"- **{category}**: {count} issues")
    report.append("")
    
    report.append("### Issues by Severity")
    severity_order = ['critical', 'high', 'medium', 'low', 'info']
    for severity in severity_order:
        if severity in issues_by_severity:
            count = len(issues_by_severity[severity])
            emoji = get_severity_emoji(severity)
            report.append(f"- {emoji} **{severity.title()}**: {count} issues")
    report.append("")
    
    report.append("### Issues by Analysis Tool")
    for tool, issues in sorted(issues_by_tool.items(), key=lambda item: len(item[1]), reverse=True):
        count = len(issues)
        tool_emoji = {'bandit': '🔒', 'radon': '🧮', 'mypy': '🔍', 'ruff': '⚡', 'flake8': '📊', 'doc-checker': '📚'}.get(tool, '🔧')
        report.append(f"- {tool_emoji} **{tool.title()}**: {count} issues")
    report.append("")
    
    report.append("### Issues by Component")
    for service, issues in sorted(issues_by_service.items(), key=lambda item: len(item[1]), reverse=True):
        count = len(issues)
        report.append(f"- **{service.replace('_', ' ').title()}**: {count} issues")
    report.append("")
    
    return report

def generate_coderabbit_audit():
    """Generate comprehensive CodeRabbit audit report"""
    print("🔍 Generating comprehensive CodeRabbit audit...")
    
    # Load analysis results
    all_issues = load_analysis_results()
    if not all_issues:
        print("⚠️  No analysis results found")
        return None
    
    print(f"✅ Found {len(all_issues)} issues to analyze")
    # Note: Full audit report generation is not yet implemented
    # This function currently serves as a placeholder for future audit functionality
    return None
    
def generate_security_analysis(issues_by_type):
    """Generate security analysis section"""
    report = []
    security_issues = issues_by_type.get('security', [])
    
    if security_issues:
        report.append("## 🔒 Security Analysis Deep Dive")
        report.append("")
        report.append(f"**Total Security Issues**: {len(security_issues)}")
        report.append("")
        
        # Group security issues by rule
        security_by_rule = defaultdict(list)
        for issue in security_issues:
            rule = issue.get('rule', 'unknown')
            security_by_rule[rule].append(issue)
        
        report.append("### Security Issues by Rule")
        for rule, rule_issues in sorted(security_by_rule.items(), key=lambda item: len(item[1]), reverse=True):
            count = len(rule_issues)
            first_issue = rule_issues[0]
            severity = first_issue.get('severity', 'unknown')
            emoji = get_severity_emoji(severity)
            
            report.append(f"#### {emoji} {rule} ({count} occurrences)")
            report.append(f"- **Typical Severity**: {severity.title()}")
            report.append(f"- **Example**: {first_issue.get('message', '')}")
            
            # Show affected services
            affected_services = set()
            for issue in rule_issues:
                service = extract_service_name(issue.get('file', ''))
                affected_services.add(service)
            
            report.append(f"- **Affected Services**: {', '.join(sorted(affected_services))}")
            report.append("")
    
    return report

def generate_action_items(issues_by_severity):
    """Generate recommended action items section"""
    report = []
    report.append("## Recommended Action Items")
    report.append("")
    
    # Critical and High Priority Actions
    critical_high_issues = len(issues_by_severity.get('critical', [])) + len(issues_by_severity.get('high', []))
    if critical_high_issues > 0:
        report.append(f"### 🚨 Immediate Action Required ({critical_high_issues} issues)")
        report.append("- Address all CRITICAL and HIGH severity issues immediately")
        report.append("- Focus on security vulnerabilities first")
        report.append("- Review shell command usage and subprocess calls")
        report.append("- Fix weak cryptographic hash usage")
        report.append("")
    
    # Medium Priority Actions
    medium_issues = len(issues_by_severity.get('medium', []))
    if medium_issues > 0:
        report.append(f"### ⚡ High Priority ({medium_issues} issues)")
        report.append("- Address MEDIUM severity issues")
        report.append("- Focus on code complexity reduction")
        report.append("- Improve type annotations")
        report.append("- Implement coding standards consistently")
        report.append("")
    
    # Code Quality Improvements
    low_issues = len(issues_by_severity.get('low', []))
    if low_issues > 0:
        report.append(f"### 🔧 Code Quality Improvements ({low_issues} issues)")
        report.append("- Address LOW severity issues")
        report.append("- Improve documentation coverage")
        report.append("- Implement automated code formatting")
        report.append("- Set up pre-commit hooks for quality checks")
        report.append("")
    
    return report

def generate_analysis_comparison(all_issues, issues_by_severity, issues_by_tool, issues_by_type):
    """Generate analysis comparison and tool usage guide"""
    report = []
    security_issues = issues_by_type.get('security', [])
    
    # Comparison with SonarQube
    report.append("## 📊 Analysis Comparison")
    report.append("")
    report.append("### CodeRabbit vs SonarQube Analysis")
    report.append("| Metric | CodeRabbit | SonarQube |")
    report.append("|--------|------------|-----------|")
    report.append(f"| Total Issues | {len(all_issues)} | 542 |")
    report.append(f"| Security Issues | {len(security_issues)} | 2 |")
    report.append(f"| High Severity | {len(issues_by_severity.get('high', []))} | 81 (Critical) |")
    report.append(f"| Analysis Tools | {len(issues_by_tool)} | 1 (SonarQube) |")
    report.append("")
    report.append("**Key Differences:**")
    report.append("- CodeRabbit uses multiple specialized tools (Bandit, Radon, MyPy, etc.)")
    report.append("- Higher issue detection due to comprehensive local analysis")
    report.append("- More granular security analysis with Bandit")
    report.append("- Includes type safety and documentation checks")
    report.append("- Local execution vs cloud-based analysis")
    report.append("")
    
    # Tool Usage Summary
    report.append("## 🛠️ Tool Usage Guide")
    report.append("")
    report.append("### Running CodeRabbit Analysis")
    report.append("```bash")
    report.append("# Quick analysis")
    report.append("python scripts/local_coderabbit.py --path . --format both")
    report.append("")
    report.append("# Using make commands")
    report.append("make -f Makefile.coderabbit coderabbit-quick")
    report.append("make -f Makefile.coderabbit coderabbit-full")
    report.append("make -f Makefile.coderabbit coderabbit-security")
    report.append("```")
    report.append("")
    report.append("### Pre-commit Integration")
    report.append("```bash")
    report.append("# Install pre-commit hooks")
    report.append("pre-commit install")
    report.append("")
    report.append("# Run pre-commit checks")
    report.append("pre-commit run --all-files")
    report.append("```")
    report.append("")
    
    return report

def save_report_and_print_summary(report_content, all_issues, issues_by_service, issues_by_tool):
    """Save report and print summary"""
    os.makedirs("reports/coderabbit", exist_ok=True)
    
    with open("reports/coderabbit/CodeRabbit_Audit20251027.md", "w") as f:
        f.write(report_content)
    
    print("✅ CodeRabbit audit report generated: reports/coderabbit/CodeRabbit_Audit20251027.md")
    print(f"📊 Total Issues Documented: {len(all_issues)}")
    print(f"🏢 Services Affected: {len(issues_by_service)}")
    print(f"🔧 Analysis Tools Used: {len(issues_by_tool)}")
    
    return report_content


if __name__ == "__main__":
    generate_coderabbit_audit()
