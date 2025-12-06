"""
SonarQube Code Quality Tests for scripts/llm_evaluation.py - Batch 2

TDD Tests for Issues 11-20:
- S1192 (Issues 11-16): Duplicated string literals - extract constants
- S3457 (Issues 17-20): Empty f-strings - remove f-prefix

Reference: CODING_PATTERNS_ANALYSIS.md Categories 14-15
Reference: Comp_Static_Analysis_Report_20251203.md Issues 47-48, 50
"""
import pytest
import re
from pathlib import Path


class TestSonarQubeBatch2DuplicatedLiterals:
    """
    Static analysis tests for S1192: Duplicated string literals.
    
    Issues 11-16: Extract constants for strings repeated 3+ times.
    Pattern Reference: CODING_PATTERNS_ANALYSIS.md Category 15
    """
    
    @pytest.fixture
    def llm_evaluation_content(self) -> str:
        """Load llm_evaluation.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def test_issue_11_application_json_constant(self, llm_evaluation_content: str):
        """
        Issue 11 (S1192 Line 100): "application/json" appears 10 times.
        Extract to CONTENT_TYPE_JSON constant.
        """
        literal_count = len(re.findall(r'"application/json"', llm_evaluation_content))
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '\"application/json\"' literal. "
            f"Extract to constant CONTENT_TYPE_JSON (SonarQube S1192)."
        )
    
    def test_issue_12_gemini_flash_constant(self, llm_evaluation_content: str):
        """
        Issue 12 (S1192 Line 127): "gemini-2.5-flash" used in config assignment.
        Extract to MODEL_GEMINI_FLASH constant and use EVERYWHERE.
        
        Per Category 15 pattern: constant must replace ALL occurrences including dict keys.
        """
        # Constant must be defined
        assert 'MODEL_GEMINI_FLASH = "gemini-2.5-flash"' in llm_evaluation_content, (
            "Missing constant definition MODEL_GEMINI_FLASH (SonarQube S1192)."
        )
        # Constant should be used in model= assignment
        assert 'model=MODEL_GEMINI_FLASH' in llm_evaluation_content, (
            "Constant MODEL_GEMINI_FLASH should be used in LLMConfig model= assignment."
        )
        # Constant should be used as dict key
        assert 'configs[MODEL_GEMINI_FLASH]' in llm_evaluation_content, (
            "Constant MODEL_GEMINI_FLASH should be used as dict key (SonarQube S1192)."
        )
        # String literal should NOT appear as dict key
        assert 'configs["gemini-2.5-flash"]' not in llm_evaluation_content, (
            "Literal 'gemini-2.5-flash' should not be used as dict key - use MODEL_GEMINI_FLASH."
        )
    
    def test_issue_13_claude_opus_constant(self, llm_evaluation_content: str):
        """
        Issue 13 (S1192 Line 140): "claude-opus-4.5" used in multiple places.
        Extract to MODEL_CLAUDE_OPUS constant and use EVERYWHERE.
        
        Per Category 15 pattern: constant must replace ALL occurrences including dict keys.
        """
        # Constant must be defined
        assert 'MODEL_CLAUDE_OPUS = "claude-opus-4.5"' in llm_evaluation_content, (
            "Missing constant definition MODEL_CLAUDE_OPUS (SonarQube S1192)."
        )
        # Constant should be used as dict key
        assert 'configs[MODEL_CLAUDE_OPUS]' in llm_evaluation_content, (
            "Constant MODEL_CLAUDE_OPUS should be used as dict key (SonarQube S1192)."
        )
        # String literal should NOT appear as dict key
        assert 'configs["claude-opus-4.5"]' not in llm_evaluation_content, (
            "Literal 'claude-opus-4.5' should not be used as dict key - use MODEL_CLAUDE_OPUS."
        )
    
    def test_issue_14_claude_sonnet_constant(self, llm_evaluation_content: str):
        """
        Issue 14 (S1192 Line 151): "claude-sonnet-4.5" used in multiple places.
        Extract to MODEL_CLAUDE_SONNET constant and use EVERYWHERE.
        
        Per Category 15 pattern: constant must replace ALL occurrences including dict keys.
        """
        # Constant must be defined
        assert 'MODEL_CLAUDE_SONNET = "claude-sonnet-4.5"' in llm_evaluation_content, (
            "Missing constant definition MODEL_CLAUDE_SONNET (SonarQube S1192)."
        )
        # Constant should be used as dict key
        assert 'configs[MODEL_CLAUDE_SONNET]' in llm_evaluation_content, (
            "Constant MODEL_CLAUDE_SONNET should be used as dict key (SonarQube S1192)."
        )
        # String literal should NOT appear as dict key
        assert 'configs["claude-sonnet-4.5"]' not in llm_evaluation_content, (
            "Literal 'claude-sonnet-4.5' should not be used as dict key - use MODEL_CLAUDE_SONNET."
        )
    
    def test_issue_15_gpt_constant(self, llm_evaluation_content: str):
        """
        Issue 15 (S1192 Line 166): "gpt-5.1" used in config assignment.
        Extract to MODEL_GPT constant and use EVERYWHERE.
        
        Per Category 15 pattern: constant must replace ALL occurrences including dict keys.
        """
        # Constant must be defined
        assert 'MODEL_GPT = "gpt-5.1"' in llm_evaluation_content, (
            "Missing constant definition MODEL_GPT (SonarQube S1192)."
        )
        # Constant should be used in model= assignment
        assert 'model=MODEL_GPT' in llm_evaluation_content, (
            "Constant MODEL_GPT should be used in LLMConfig model= assignment."
        )
        # Constant should be used as dict key
        assert 'configs[MODEL_GPT]' in llm_evaluation_content, (
            "Constant MODEL_GPT should be used as dict key (SonarQube S1192)."
        )
        # String literal should NOT appear as dict key
        assert 'configs["gpt-5.1"]' not in llm_evaluation_content, (
            "Literal 'gpt-5.1' should not be used as dict key - use MODEL_GPT."
        )
    
    def test_issue_16_json_code_block_constant(self, llm_evaluation_content: str):
        """
        Issue 16 (S1192 Line 394): "```json" appears 4 times.
        Extract to JSON_CODE_BLOCK constant.
        """
        # Escape the backticks in regex
        literal_count = len(re.findall(r'["\']```json["\']', llm_evaluation_content))
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '```json' literal. "
            f"Extract to constant JSON_CODE_BLOCK (SonarQube S1192)."
        )


class TestSonarQubeBatch2EmptyFStrings:
    """
    Static analysis tests for S3457: Empty f-strings.
    
    Issues 17-20: Remove f-prefix when no placeholders used.
    Pattern Reference: CODING_PATTERNS_ANALYSIS.md Category 14
    """
    
    @pytest.fixture
    def llm_evaluation_content(self) -> str:
        """Load llm_evaluation.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def _get_line_content(self, content: str, line_num: int) -> str:
        """Get content of a specific line."""
        lines = content.split('\n')
        if 0 < line_num <= len(lines):
            return lines[line_num - 1]
        return ""
    
    def _has_empty_fstring(self, line: str) -> bool:
        """Check if line contains an f-string without placeholders."""
        # Match f"..." or f'...' patterns
        fstring_matches = re.findall(r'f["\']([^"\']*)["\']', line)
        for match in fstring_matches:
            if '{' not in match:
                return True
        return False
    
    def test_issue_17_line_661_no_empty_fstring(self, llm_evaluation_content: str):
        """
        Issue 17 (S3457 Line 661): Empty f-string.
        Remove f-prefix when no placeholders used.
        """
        line = self._get_line_content(llm_evaluation_content, 661)
        assert not self._has_empty_fstring(line), (
            f"Line 661 contains empty f-string. "
            f"Remove f-prefix (SonarQube S3457). Line: {line.strip()}"
        )
    
    def test_issue_18_line_1457_no_empty_fstring(self, llm_evaluation_content: str):
        """
        Issue 18 (S3457 Line 1457): Empty f-string.
        Remove f-prefix when no placeholders used.
        """
        line = self._get_line_content(llm_evaluation_content, 1457)
        assert not self._has_empty_fstring(line), (
            f"Line 1457 contains empty f-string. "
            f"Remove f-prefix (SonarQube S3457). Line: {line.strip()}"
        )
    
    def test_issue_19_line_1472_no_empty_fstring(self, llm_evaluation_content: str):
        """
        Issue 19 (S3457 Line 1472): Empty f-string.
        Remove f-prefix when no placeholders used.
        """
        line = self._get_line_content(llm_evaluation_content, 1472)
        assert not self._has_empty_fstring(line), (
            f"Line 1472 contains empty f-string. "
            f"Remove f-prefix (SonarQube S3457). Line: {line.strip()}"
        )
    
    def test_issue_20_line_1542_no_empty_fstring(self, llm_evaluation_content: str):
        """
        Issue 20 (S3457 Line 1542): Empty f-string.
        Remove f-prefix when no placeholders used.
        """
        line = self._get_line_content(llm_evaluation_content, 1542)
        assert not self._has_empty_fstring(line), (
            f"Line 1542 contains empty f-string. "
            f"Remove f-prefix (SonarQube S3457). Line: {line.strip()}"
        )


class TestBatch2ConstantDefinitions:
    """
    Positive tests to verify constants are properly defined after fixes.
    """
    
    @pytest.fixture
    def llm_evaluation_content(self) -> str:
        """Load llm_evaluation.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def test_has_content_type_constant(self, llm_evaluation_content: str):
        """Verify CONTENT_TYPE_JSON constant is defined."""
        assert re.search(
            r'^CONTENT_TYPE_JSON\s*=\s*["\']application/json["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected CONTENT_TYPE_JSON constant to be defined"
    
    def test_has_model_gemini_constant(self, llm_evaluation_content: str):
        """Verify MODEL_GEMINI_FLASH constant is defined."""
        assert re.search(
            r'^MODEL_GEMINI_FLASH\s*=\s*["\']gemini-2\.5-flash["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected MODEL_GEMINI_FLASH constant to be defined"
    
    def test_has_model_claude_opus_constant(self, llm_evaluation_content: str):
        """Verify MODEL_CLAUDE_OPUS constant is defined."""
        assert re.search(
            r'^MODEL_CLAUDE_OPUS\s*=\s*["\']claude-opus-4\.5["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected MODEL_CLAUDE_OPUS constant to be defined"
    
    def test_has_model_claude_sonnet_constant(self, llm_evaluation_content: str):
        """Verify MODEL_CLAUDE_SONNET constant is defined."""
        assert re.search(
            r'^MODEL_CLAUDE_SONNET\s*=\s*["\']claude-sonnet-4\.5["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected MODEL_CLAUDE_SONNET constant to be defined"
    
    def test_has_model_gpt_constant(self, llm_evaluation_content: str):
        """Verify MODEL_GPT constant is defined."""
        assert re.search(
            r'^MODEL_GPT\s*=\s*["\']gpt-5\.1["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected MODEL_GPT constant to be defined"
    
    def test_has_json_code_block_constant(self, llm_evaluation_content: str):
        """Verify JSON_CODE_BLOCK constant is defined."""
        assert re.search(
            r'^JSON_CODE_BLOCK\s*=\s*["\']```json["\']',
            llm_evaluation_content,
            re.MULTILINE
        ), "Expected JSON_CODE_BLOCK constant to be defined"


class TestRemainingS1192Issues:
    """
    TDD RED tests for remaining S1192 duplicated literal issues in llm_evaluation.py.
    
    SonarQube reports 6 remaining S1192 issues at lines:
    - Line 176: "https://api.openai.com/v1/chat/completions" (4 times)
    - Line 289: System prompt for NLP evaluation (3-5 times)
    - Line 317: "Failed to parse JSON" (5 times)
    - Line 323: "Rate limited (429) - too many requests" (3+ times)
    - Line 325: "Authentication failed (401) - check API key" (4 times)
    - Line 844: "static analysis" (4 times)
    
    Reference: CODING_PATTERNS_ANALYSIS.md Category 15 (Duplicated Literals)
    Reference: Comp_Static_Analysis_Report_20251203.md Issue 50
    """
    
    @pytest.fixture
    def llm_evaluation_content(self) -> str:
        """Load llm_evaluation.py content for analysis."""
        file_path = Path(__file__).parent.parent.parent.parent / "scripts" / "llm_evaluation.py"
        return file_path.read_text()
    
    def test_openai_api_url_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 176: "https://api.openai.com/v1/chat/completions" appears 4 times.
        Extract to OPENAI_CHAT_COMPLETIONS_URL constant.
        """
        literal = "https://api.openai.com/v1/chat/completions"
        literal_count = llm_evaluation_content.count(f'"{literal}"')
        
        # Constant should be defined
        assert 'OPENAI_CHAT_COMPLETIONS_URL' in llm_evaluation_content, (
            f"Missing constant OPENAI_CHAT_COMPLETIONS_URL for duplicated literal (S1192)."
        )
        
        # Literal should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '{literal}'. "
            f"Use constant OPENAI_CHAT_COMPLETIONS_URL instead (S1192)."
        )
    
    def test_evaluation_system_prompt_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 289: System prompt for NLP evaluation appears 3+ times.
        Extract to EVALUATION_SYSTEM_PROMPT constant.
        """
        # Look for the exact system prompt pattern
        prompt_pattern = "You are an expert at evaluating NLP extraction quality. You MUST respond with valid JSON only."
        literal_count = llm_evaluation_content.count(prompt_pattern)
        
        # Constant should be defined
        assert 'EVALUATION_SYSTEM_PROMPT' in llm_evaluation_content, (
            f"Missing constant EVALUATION_SYSTEM_PROMPT for duplicated system prompt (S1192)."
        )
        
        # Full prompt should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of evaluation system prompt. "
            f"Use constant EVALUATION_SYSTEM_PROMPT instead (S1192)."
        )
    
    def test_failed_to_parse_json_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 317: "Failed to parse JSON" appears 5 times.
        Extract to ERROR_FAILED_TO_PARSE_JSON constant.
        """
        literal = "Failed to parse JSON"
        literal_count = llm_evaluation_content.count(f'"{literal}"')
        
        # Constant should be defined
        assert 'ERROR_FAILED_TO_PARSE_JSON' in llm_evaluation_content, (
            f"Missing constant ERROR_FAILED_TO_PARSE_JSON for duplicated literal (S1192)."
        )
        
        # Literal should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '{literal}'. "
            f"Use constant ERROR_FAILED_TO_PARSE_JSON instead (S1192)."
        )
    
    def test_rate_limited_error_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 323: "Rate limited (429) - too many requests" appears 3+ times.
        Extract to ERROR_RATE_LIMITED constant.
        """
        literal = "Rate limited (429) - too many requests"
        literal_count = llm_evaluation_content.count(f'"{literal}"')
        
        # Constant should be defined
        assert 'ERROR_RATE_LIMITED' in llm_evaluation_content, (
            f"Missing constant ERROR_RATE_LIMITED for duplicated literal (S1192)."
        )
        
        # Literal should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '{literal}'. "
            f"Use constant ERROR_RATE_LIMITED instead (S1192)."
        )
    
    def test_auth_failed_error_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 325: "Authentication failed (401) - check API key" appears 4 times.
        Extract to ERROR_AUTH_FAILED constant.
        """
        literal = "Authentication failed (401) - check API key"
        literal_count = llm_evaluation_content.count(f'"{literal}"')
        
        # Constant should be defined  
        assert 'ERROR_AUTH_FAILED' in llm_evaluation_content, (
            f"Missing constant ERROR_AUTH_FAILED for duplicated literal (S1192)."
        )
        
        # Literal should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '{literal}'. "
            f"Use constant ERROR_AUTH_FAILED instead (S1192)."
        )
    
    def test_static_analysis_constant(self, llm_evaluation_content: str):
        """
        S1192 Line 844: "static analysis" appears 4 times.
        Extract to KEYWORD_STATIC_ANALYSIS constant.
        """
        literal = "static analysis"
        literal_count = llm_evaluation_content.count(f'"{literal}"')
        
        # Constant should be defined
        assert 'KEYWORD_STATIC_ANALYSIS' in llm_evaluation_content, (
            f"Missing constant KEYWORD_STATIC_ANALYSIS for duplicated literal (S1192)."
        )
        
        # Literal should appear at most once (in constant definition)
        assert literal_count <= 1, (
            f"Found {literal_count} occurrences of '{literal}'. "
            f"Use constant KEYWORD_STATIC_ANALYSIS instead (S1192)."
        )
