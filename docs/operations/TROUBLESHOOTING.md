# LLM Document Enhancer - Troubleshooting Guide

**Version:** 1.0.0  
**Last Updated:** 2025-05-30  
**Audience:** Developers, Operations, Support  

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Common Issues](#common-issues)
3. [Error Reference](#error-reference)
4. [Debugging Techniques](#debugging-techniques)
5. [Connectivity Issues](#connectivity-issues)
6. [Performance Problems](#performance-problems)
7. [LLM Provider Issues](#llm-provider-issues)
8. [Log Analysis](#log-analysis)
9. [FAQ](#faq)
10. [Getting Help](#getting-help)

---

## Quick Diagnostics

### Health Check Script

Run this script to quickly diagnose common issues:

```bash
#!/bin/bash
# quick_diagnostic.sh

echo "=== LLM Document Enhancer Diagnostics ==="
echo ""

# 1. Check Python environment
echo "1. Python Environment"
python --version || echo "  ❌ Python not found"
pip --version || echo "  ❌ pip not found"
echo ""

# 2. Check process status
echo "2. Service Status"
if pgrep -f "run_pipeline.py" > /dev/null; then
    echo "  ✅ Pipeline process running"
else
    echo "  ⚠️  Pipeline process not running"
fi
echo ""

# 3. Check API keys
echo "3. API Keys"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "  ✅ OPENAI_API_KEY is set"
else
    echo "  ⚠️  OPENAI_API_KEY not set"
fi
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "  ✅ ANTHROPIC_API_KEY is set"
else
    echo "  ⚠️  ANTHROPIC_API_KEY not set"
fi
echo ""

# 4. Check disk space
echo "4. Disk Space"
df -h . | awk 'NR==2 {print "  Used: " $5 " of " $2}'
echo ""

# 5. Check recent errors
echo "5. Recent Errors (last 10)"
if [ -f logs/observability/app.log ]; then
    grep -i error logs/observability/app.log | tail -5 || echo "  No recent errors"
else
    echo "  Log file not found"
fi
echo ""

# 6. Check dependencies
echo "6. Dependencies"
pip check 2>/dev/null && echo "  ✅ No dependency conflicts" || echo "  ⚠️  Dependency issues found"
echo ""

echo "=== Diagnostics Complete ==="
```

### System Requirements Check

```bash
# Verify Python version (3.9+ required)
python --version

# Check available memory
free -m

# Check disk space
df -h /path/to/llm-document-enhancer

# Verify required packages
pip list | grep -E "openai|anthropic|pdfplumber|pydantic"
```

---

## Common Issues

### Issue: Service Won't Start

#### Symptoms
- Pipeline process doesn't start
- Immediate exit after starting
- No log files created

#### Diagnosis

```bash
# Try running directly to see errors
python scripts/run_pipeline.py 2>&1

# Check Python path
which python
echo $PYTHONPATH

# Check for import errors
python -c "import config.settings; print('Config OK')"
```

#### Solutions

| Cause | Solution |
|-------|----------|
| Missing dependencies | `pip install -r requirements.txt` |
| Wrong Python version | Use Python 3.9+ |
| Missing config files | Copy from `config/*.example` |
| Invalid config syntax | Validate JSON: `python -m json.tool config/*.json` |
| Permission denied | `chmod +x scripts/*.py` |

---

### Issue: Document Processing Fails

#### Symptoms
- Specific documents fail to process
- "Unable to extract text" errors
- Empty output files

#### Diagnosis

```bash
# Test PDF extraction manually
python -c "
import pdfplumber
with pdfplumber.open('path/to/document.pdf') as pdf:
    for page in pdf.pages[:3]:
        text = page.extract_text()
        print(f'Page {page.page_number}: {len(text) if text else 0} chars')
"
```

#### Solutions

| Cause | Solution |
|-------|----------|
| Corrupt PDF | Re-download or recreate PDF |
| Scanned PDF (images only) | Use OCR preprocessing |
| Password protected | Decrypt before processing |
| Unsupported PDF version | Convert to standard PDF |
| Large file timeout | Increase timeout in settings |

```bash
# For scanned PDFs, try OCR first
pip install pytesseract pdf2image
python scripts/ocr_pdf.py input.pdf output.pdf
```

---

### Issue: API Key Errors

#### Symptoms
- "Invalid API key" errors
- "Authentication failed" responses
- 401/403 HTTP errors

#### Diagnosis

```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -s | head -20

# Test Anthropic key
curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}' \
    -s | head -20
```

#### Solutions

| Cause | Solution |
|-------|----------|
| Key not set | `export OPENAI_API_KEY="sk-..."` |
| Key expired | Generate new key in provider dashboard |
| Key has wrong permissions | Check API key scopes |
| Billing issue | Add payment method to account |
| Key in wrong format | Remove quotes/whitespace |

```bash
# Verify key format (OpenAI)
echo $OPENAI_API_KEY | grep -E "^sk-[a-zA-Z0-9]{48}$" && echo "Format OK"

# Set key properly
export OPENAI_API_KEY="sk-your-actual-key-here"
```

---

### Issue: Rate Limit Errors

#### Symptoms
- "Rate limit exceeded" errors
- 429 HTTP status codes
- Processing slows dramatically

#### Diagnosis

```bash
# Check recent rate limit errors
grep -i "rate.limit\|429" logs/observability/app.log | tail -20

# Count requests per minute
grep "LLM API call" logs/llm_api/*.log | \
    awk -F'T' '{print $1, substr($2,1,5)}' | \
    uniq -c | sort -rn | head -10
```

#### Solutions

```python
# config/settings.py - Reduce rate
LLM_CONFIG = {
    "rate_limit": 30,  # Reduce from 60
    "retry_attempts": 5,  # Increase retries
    "retry_delay": 2.0,  # Longer delay
}
```

| Cause | Solution |
|-------|----------|
| Too many concurrent requests | Reduce `rate_limit` setting |
| Burst of requests | Add delays between batches |
| Account tier limit | Upgrade API plan |
| Shared API key | Use dedicated key |

---

### Issue: Out of Memory

#### Symptoms
- "MemoryError" exceptions
- Process killed by OS
- Slow performance then crash

#### Diagnosis

```bash
# Monitor memory during processing
watch -n 1 'ps aux | grep run_pipeline.py | awk "{print \$4\"%\"}"'

# Check system memory
free -m

# Check for memory leaks
python -c "
import tracemalloc
tracemalloc.start()
# Run your code
current, peak = tracemalloc.get_traced_memory()
print(f'Current: {current / 10**6:.1f} MB, Peak: {peak / 10**6:.1f} MB')
"
```

#### Solutions

| Cause | Solution |
|-------|----------|
| Large PDF files | Process in chunks |
| Memory leaks | Update dependencies |
| Too many concurrent jobs | Reduce `MAX_WORKERS` |
| Large response caching | Reduce cache size |

```python
# Process large documents in chunks
def process_large_pdf(pdf_path, chunk_size=50):
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(0, len(pdf.pages), chunk_size):
            chunk = pdf.pages[i:i+chunk_size]
            process_chunk(chunk)
            gc.collect()  # Force garbage collection
```

---

### Issue: Slow Processing

#### Symptoms
- Documents take too long to process
- Queue builds up
- Timeouts

#### Diagnosis

```bash
# Profile processing time
python -m cProfile -s cumulative scripts/run_pipeline.py 2>&1 | head -50

# Check which step is slow
grep "processing_time\|step_time" logs/observability/app.log | tail -20

# Monitor network latency
ping api.openai.com -c 5
```

#### Solutions

| Cause | Solution |
|-------|----------|
| Network latency | Check connectivity |
| LLM response time | Use faster model |
| Large documents | Process in parallel |
| No caching | Enable response cache |
| Cold start | Pre-warm connections |

```python
# Enable caching
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,
    "max_size": 1000,
}
```

---

## Error Reference

### Error Code Index

| Error Code | Description | Quick Fix |
|------------|-------------|-----------|
| `ERR_001` | Configuration file not found | Check config/ directory |
| `ERR_002` | Invalid configuration format | Validate JSON syntax |
| `ERR_003` | API key not configured | Set environment variable |
| `ERR_004` | API authentication failed | Verify API key |
| `ERR_005` | Rate limit exceeded | Wait and retry |
| `ERR_006` | Network connection failed | Check connectivity |
| `ERR_007` | PDF extraction failed | Check PDF format |
| `ERR_008` | LLM response parsing error | Check prompt format |
| `ERR_009` | Output validation failed | Check output schema |
| `ERR_010` | Disk space insufficient | Clean old files |

### Detailed Error Descriptions

#### ERR_001: Configuration File Not Found

```
Error: Configuration file not found: config/settings.py
```

**Cause:** Required configuration file is missing.

**Fix:**
```bash
# Check what config files exist
ls -la config/

# Copy example config
cp config/settings.example.py config/settings.py

# Or create from template
python scripts/generate_config.py
```

---

#### ERR_003: API Key Not Configured

```
Error: API key not configured for provider 'openai'
```

**Cause:** LLM API key not found in environment.

**Fix:**
```bash
# Set for current session
export OPENAI_API_KEY="sk-..."

# Or add to .env file
echo 'OPENAI_API_KEY=sk-...' >> .env

# Verify it's set
python -c "import os; print('Key set:', bool(os.getenv('OPENAI_API_KEY')))"
```

---

#### ERR_005: Rate Limit Exceeded

```
Error: Rate limit exceeded. Retry after 60 seconds.
```

**Cause:** Too many API requests in short period.

**Fix:**
```bash
# Wait and retry
sleep 60 && python scripts/run_pipeline.py

# Or reduce rate limit in config
# config/settings.py: rate_limit = 30
```

---

#### ERR_007: PDF Extraction Failed

```
Error: Failed to extract text from document.pdf: PDFSyntaxError
```

**Cause:** PDF file is corrupted or uses unsupported features.

**Fix:**
```bash
# Verify PDF
pdfinfo document.pdf

# Try repairing
pdftk document.pdf output repaired.pdf

# Convert to standard format
pdf2ps document.pdf - | ps2pdf - standard.pdf
```

---

#### ERR_008: LLM Response Parsing Error

```
Error: Failed to parse LLM response: JSONDecodeError
```

**Cause:** LLM returned malformed or unexpected response.

**Fix:**
```python
# Enable debug logging to see raw responses
import logging
logging.getLogger("llm_client").setLevel(logging.DEBUG)

# Check raw response
with open("logs/llm_api/last_response.json") as f:
    print(f.read())
```

---

## Debugging Techniques

### Enable Debug Logging

```python
# config/settings.py
LOG_LEVEL = "DEBUG"

# Or via environment
export LOG_LEVEL=DEBUG
python scripts/run_pipeline.py
```

### Interactive Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()

# Run with debugger
python -m pdb scripts/run_pipeline.py
```

### Log Tracing

```bash
# Trace specific document through logs
DOC_ID="12345"
grep "$DOC_ID" logs/observability/app.log | less

# Follow log for specific component
tail -f logs/observability/app.log | grep -i "extraction"
```

### Dry Run Mode

```bash
# Run without making API calls
python scripts/run_pipeline.py --dry-run

# Process single document for testing
python scripts/run_pipeline.py --single-file test.pdf --verbose
```

### Unit Test Debugging

```bash
# Run specific test with output
python -m pytest tests_unit/test_extraction.py -v -s

# Run with debugger on failure
python -m pytest tests_unit/ --pdb

# Run with coverage to find untested code
python -m pytest tests_unit/ --cov=src --cov-report=html
```

---

## Connectivity Issues

### Network Diagnostics

```bash
# Test DNS resolution
nslookup api.openai.com

# Test connectivity
curl -I https://api.openai.com/v1/models

# Test with verbose output
curl -v https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"

# Check for proxy issues
echo $HTTP_PROXY $HTTPS_PROXY
```

### Firewall Issues

```bash
# Check if ports are open
nc -zv api.openai.com 443

# Test through different methods
wget --spider https://api.openai.com
```

### Proxy Configuration

```bash
# Set proxy if required
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
export NO_PROXY="localhost,127.0.0.1"

# Or configure in Python
import os
os.environ["HTTP_PROXY"] = "http://proxy:8080"
```

### SSL/TLS Issues

```bash
# Check SSL certificate
openssl s_client -connect api.openai.com:443 -servername api.openai.com

# Update CA certificates
pip install --upgrade certifi

# Verify Python's certificate store
python -c "import ssl; print(ssl.get_default_verify_paths())"
```

---

## Performance Problems

### Profiling

```bash
# CPU profiling
python -m cProfile -o profile.stats scripts/run_pipeline.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Memory profiling
pip install memory_profiler
python -m memory_profiler scripts/run_pipeline.py

# Line-by-line profiling
pip install line_profiler
kernprof -l -v scripts/run_pipeline.py
```

### Bottleneck Identification

| Symptom | Likely Bottleneck | Investigation |
|---------|-------------------|---------------|
| CPU at 100% | PDF parsing, regex | Profile CPU |
| High memory | Large documents, caching | Profile memory |
| Network waiting | LLM API latency | Check connectivity |
| Disk I/O | Large files, logging | Monitor I/O |

### Performance Optimization Checklist

- [ ] Enable response caching
- [ ] Use batch processing for multiple documents
- [ ] Reduce logging verbosity in production
- [ ] Use faster LLM model for simple tasks
- [ ] Process large PDFs in chunks
- [ ] Enable connection pooling
- [ ] Use async processing where possible

---

## LLM Provider Issues

### OpenAI Issues

#### Check Status

```bash
# API status
curl -s https://status.openai.com/api/v2/status.json | jq .status

# Model availability
curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[].id' | head -10
```

#### Common OpenAI Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `insufficient_quota` | Account has no credits | Add billing |
| `model_not_found` | Invalid model name | Check model name |
| `context_length_exceeded` | Input too long | Reduce document size |
| `server_error` | OpenAI issue | Wait and retry |

### Anthropic Issues

#### Check Status

```bash
# Test connectivity
curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

#### Common Anthropic Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_api_key` | Wrong API key | Check key format |
| `rate_limit_error` | Too many requests | Add delays |
| `overloaded_error` | Service busy | Retry with backoff |

### Provider Fallback

```python
# config/settings.py - Configure fallback
LLM_PROVIDERS = {
    "primary": "openai",
    "fallback": "anthropic",
    "auto_fallback": True,
}
```

---

## Log Analysis

### Log File Locations

```
logs/
├── observability/
│   ├── app.log          # Main application log
│   ├── error.log        # Errors only
│   └── audit.log        # Security/audit events
└── llm_api/
    └── api_calls.log    # LLM API interactions
```

### Log Format

```
2025-05-30 12:00:00,123 | INFO | module.name | Message | {"context": "data"}
```

### Useful Log Queries

```bash
# Find all errors in last hour
grep "ERROR" logs/observability/app.log | \
    awk -v threshold="$(date -d '1 hour ago' '+%Y-%m-%d %H:%M')" \
    '$1" "$2 > threshold'

# Count errors by type
grep "ERROR" logs/observability/app.log | \
    sed 's/.*ERROR.*| \([^|]*\) |.*/\1/' | \
    sort | uniq -c | sort -rn

# Find slow operations (>5s)
grep "duration" logs/observability/app.log | \
    awk -F'duration=' '{if($2>5000) print}'

# Track specific request
grep "request_id=abc123" logs/observability/app.log

# Find memory warnings
grep -i "memory\|MemoryError" logs/observability/app.log
```

### Log Aggregation

```bash
# Combine logs for analysis
cat logs/observability/*.log | sort > combined.log

# Generate summary report
cat combined.log | \
    awk '{print $4}' | \
    sort | uniq -c | \
    sort -rn > log_summary.txt
```

---

## FAQ

### General Questions

**Q: What Python version is required?**

A: Python 3.9 or higher. Check with `python --version`.

---

**Q: How do I update to the latest version?**

A:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Q: Where are processed documents stored?**

A: In the `outputs/` directory, organized by date/batch.

---

**Q: How do I process a single document for testing?**

A:
```bash
python scripts/run_pipeline.py --single-file document.pdf --verbose
```

---

### Configuration Questions

**Q: How do I change the LLM provider?**

A: Set the `LLM_PROVIDER` environment variable:
```bash
export LLM_PROVIDER=anthropic  # or openai
```

---

**Q: How do I enable caching?**

A: In `config/settings.py`:
```python
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,
}
```

---

**Q: How do I reduce API costs?**

A: 
- Enable caching to avoid duplicate requests
- Use `gpt-4o-mini` instead of `gpt-4o` for simpler tasks
- Reduce token limits in prompts
- Batch similar documents together

---

### Troubleshooting Questions

**Q: Why is processing so slow?**

A: Common causes:
1. Network latency to LLM provider
2. Large documents
3. No caching enabled
4. Debug logging enabled

Check with: `python -m cProfile scripts/run_pipeline.py`

---

**Q: Why do I get empty outputs?**

A: Check:
1. PDF contains extractable text (not just images)
2. LLM API is responding correctly
3. Output validation isn't filtering everything

Test extraction: 
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    print(pdf.pages[0].extract_text()[:500])
```

---

**Q: How do I reset everything and start fresh?**

A:
```bash
# Clear outputs
rm -rf outputs/*

# Clear cache
rm -rf cache/*

# Clear logs (optional)
rm -rf logs/*

# Restore default config
cp config/*.example.json config/
```

---

**Q: How do I report a bug?**

A: 
1. Collect diagnostic info: `./scripts/quick_diagnostic.sh > diagnostic.txt`
2. Include error messages from logs
3. Create issue on GitHub with steps to reproduce

---

## Getting Help

### Support Channels

| Channel | Best For | Response Time |
|---------|----------|---------------|
| GitHub Issues | Bugs, features | 1-3 days |
| Documentation | Self-service | Immediate |
| Slack #llm-enhancer | Quick questions | Hours |

### Information to Include

When asking for help, provide:

1. **Error message** (full text)
2. **Steps to reproduce**
3. **Environment info**:
   ```bash
   python --version
   pip list | grep -E "openai|anthropic|pdfplumber"
   uname -a
   ```
4. **Relevant logs** (sanitize API keys!)
5. **Configuration** (without secrets)

### Diagnostic Information Script

```bash
#!/bin/bash
# collect_diagnostic.sh

echo "=== Diagnostic Information ===" > diagnostic.txt
echo "" >> diagnostic.txt

echo "### System Info" >> diagnostic.txt
uname -a >> diagnostic.txt
echo "" >> diagnostic.txt

echo "### Python Version" >> diagnostic.txt
python --version >> diagnostic.txt
echo "" >> diagnostic.txt

echo "### Installed Packages" >> diagnostic.txt
pip list >> diagnostic.txt
echo "" >> diagnostic.txt

echo "### Environment Variables (sanitized)" >> diagnostic.txt
env | grep -E "^(LLM_|LOG_|CACHE_)" | sed 's/=.*/=***/' >> diagnostic.txt
echo "" >> diagnostic.txt

echo "### Recent Errors" >> diagnostic.txt
grep ERROR logs/observability/app.log 2>/dev/null | tail -20 >> diagnostic.txt
echo "" >> diagnostic.txt

echo "### Disk Space" >> diagnostic.txt
df -h . >> diagnostic.txt
echo "" >> diagnostic.txt

echo "Diagnostic info saved to diagnostic.txt"
echo "Please review and redact any sensitive information before sharing."
```

---

### Quick Reference Card

```
╔══════════════════════════════════════════════════════════════════╗
║              LLM Document Enhancer - Quick Reference             ║
╠══════════════════════════════════════════════════════════════════╣
║ START SERVICE                                                     ║
║   python scripts/run_pipeline.py                                 ║
║                                                                   ║
║ CHECK STATUS                                                      ║
║   pgrep -f "run_pipeline.py"                                     ║
║                                                                   ║
║ VIEW LOGS                                                         ║
║   tail -f logs/observability/app.log                             ║
║                                                                   ║
║ FIND ERRORS                                                       ║
║   grep ERROR logs/observability/app.log | tail -20               ║
║                                                                   ║
║ TEST API KEY                                                      ║
║   curl https://api.openai.com/v1/models \                        ║
║       -H "Authorization: Bearer $OPENAI_API_KEY"                 ║
║                                                                   ║
║ DEBUG MODE                                                        ║
║   export LOG_LEVEL=DEBUG && python scripts/run_pipeline.py       ║
║                                                                   ║
║ COMMON FIXES                                                      ║
║   - pip install -r requirements.txt  (dependency issues)         ║
║   - export OPENAI_API_KEY="sk-..."   (API key issues)            ║
║   - rm -rf cache/*                   (cache issues)              ║
╚══════════════════════════════════════════════════════════════════╝
```

---

*Last reviewed: 2025-05-30*
