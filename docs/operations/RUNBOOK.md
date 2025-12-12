# LLM Document Enhancer - Operations Runbook

**Version:** 1.0.0  
**Last Updated:** 2025-05-30  
**Audience:** Operations Engineers, SREs, DevOps  

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Reference](#architecture-reference)
3. [Service Management](#service-management)
4. [Health Monitoring](#health-monitoring)
5. [Log Management](#log-management)
6. [Scaling Procedures](#scaling-procedures)
7. [Backup and Recovery](#backup-and-recovery)
8. [Deployment Procedures](#deployment-procedures)
9. [Emergency Procedures](#emergency-procedures)
10. [Maintenance Windows](#maintenance-windows)
11. [Appendix](#appendix)

---

## Overview

### Purpose

This runbook provides operational procedures for the LLM Document Enhancer service. It covers routine operations, incident response, and maintenance tasks.

### Service Description

The LLM Document Enhancer is a document processing pipeline that uses Large Language Models to extract, enrich, and validate metadata from documents (primarily PDF files).

### Key Components

| Component | Description | Port | Health Endpoint |
|-----------|-------------|------|-----------------|
| Pipeline Service | Main document processing service | N/A | N/A |
| Observability Platform | Logging and metrics | 8080 | `/health` |
| Redis (Optional) | Session/cache storage | 6379 | `PING` |
| LLM Provider | External API (OpenAI/Anthropic) | N/A | Provider status page |

### Service Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                  LLM Document Enhancer                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  │   Pipeline   │───▶│   Config     │───▶│   LLM API    │
│  │   Runner     │    │   Module     │    │   Client     │
│  └──────────────┘    └──────────────┘    └──────────────┘
│         │                   │                    │
│         ▼                   ▼                    ▼
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  │   PDF Files  │    │   JSON/YAML  │    │   OpenAI/    │
│  │   (Input)    │    │   Configs    │    │   Anthropic  │
│  └──────────────┘    └──────────────┘    └──────────────┘
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Architecture Reference

### Directory Structure

```
llm-document-enhancer/
├── config/                 # Configuration files
│   ├── settings.py         # Main settings
│   ├── chapter_patterns.json
│   ├── extraction_profiles.json
│   └── validation_rules.json
├── outputs/                # Processing outputs
├── logs/                   # Application logs
│   ├── llm_api/            # LLM API call logs
│   └── observability/      # System metrics
├── cache/                  # Response cache
│   └── llm_responses/      # Cached LLM responses
├── backups/                # Automated backups
└── observability_platform/ # Monitoring components
```

### Configuration Files

| File | Purpose | Reload Required |
|------|---------|-----------------|
| `config/settings.py` | Main configuration | Yes |
| `config/chapter_patterns.json` | Chapter detection patterns | No |
| `config/extraction_profiles.json` | Metadata extraction rules | No |
| `config/validation_rules.json` | Output validation rules | No |
| `config/metadata_keywords.json` | Keyword definitions | No |

---

## Service Management

### Starting the Service

#### Interactive Mode (Desktop)

```bash
# Double-click or run from terminal
./run_desktop.command
```

#### Command Line

```bash
# Navigate to project directory
cd /path/to/llm-document-enhancer

# Activate virtual environment (if using)
source venv/bin/activate

# Run pipeline with defaults
python scripts/run_pipeline.py

# Run with specific configuration
python scripts/run_pipeline.py --config config/settings.py --input /path/to/documents
```

#### Run with Environment Variables

```bash
# Set required environment variables
export OPENAI_API_KEY="sk-..."
export LLM_PROVIDER="openai"
export LOG_LEVEL="INFO"

# Run pipeline
python scripts/run_pipeline.py
```

### Stopping the Service

#### Graceful Shutdown

```bash
# Send SIGTERM for graceful shutdown
kill -SIGTERM <PID>

# Or use pkill
pkill -f "run_pipeline.py"
```

#### Force Stop (Emergency Only)

```bash
# Force kill - use only if graceful shutdown fails
kill -9 <PID>

# Warning: This may leave files in inconsistent state
```

### Restarting the Service

```bash
# Graceful restart
pkill -f "run_pipeline.py" && sleep 5 && python scripts/run_pipeline.py &
```

### Checking Service Status

```bash
# Check if process is running
pgrep -f "run_pipeline.py"

# Get detailed process info
ps aux | grep "run_pipeline.py"

# Check resource usage
top -p $(pgrep -f "run_pipeline.py")
```

---

## Health Monitoring

### Health Check Endpoints

#### Observability Platform Health

```bash
# Basic health check
curl -s http://localhost:8080/health

# Expected response:
# {"status": "healthy", "timestamp": "2025-05-30T12:00:00Z"}

# Detailed health with dependencies
curl -s http://localhost:8080/health/detailed
```

### Automated Health Checks

#### Health Check Script

```bash
#!/bin/bash
# health_check.sh - Automated health monitoring

HEALTH_URL="http://localhost:8080/health"
ALERT_EMAIL="ops@example.com"

check_health() {
    response=$(curl -s -w "%{http_code}" -o /tmp/health.json "$HEALTH_URL")
    
    if [ "$response" != "200" ]; then
        echo "UNHEALTHY: HTTP $response"
        send_alert "LLM Document Enhancer health check failed: HTTP $response"
        return 1
    fi
    
    status=$(jq -r '.status' /tmp/health.json)
    if [ "$status" != "healthy" ]; then
        echo "UNHEALTHY: Status is $status"
        send_alert "LLM Document Enhancer degraded: $status"
        return 1
    fi
    
    echo "HEALTHY"
    return 0
}

send_alert() {
    echo "$1" | mail -s "Alert: LLM Document Enhancer" "$ALERT_EMAIL"
}

check_health
```

### Key Metrics to Monitor

| Metric | Warning Threshold | Critical Threshold | Action |
|--------|-------------------|--------------------| -------|
| CPU Usage | > 70% | > 90% | Scale up or investigate |
| Memory Usage | > 75% | > 90% | Restart or increase memory |
| Disk Space | > 80% | > 95% | Clean old files |
| LLM API Errors | > 5% | > 10% | Check API status |
| Processing Queue | > 100 items | > 500 items | Scale up workers |
| Response Latency | > 5s | > 30s | Investigate bottleneck |

### Monitoring Commands

```bash
# Check disk space for outputs
df -h /path/to/llm-document-enhancer/outputs

# Check log file sizes
du -sh logs/*

# Monitor real-time resource usage
watch -n 5 'ps aux | grep run_pipeline.py'

# Check recent error count
grep -c "ERROR" logs/observability/app.log | tail -1
```

---

## Log Management

### Log Locations

| Log Type | Location | Rotation | Retention |
|----------|----------|----------|-----------|
| Application | `logs/observability/app.log` | Daily | 30 days |
| LLM API Calls | `logs/llm_api/*.log` | Per run | 7 days |
| Error Log | `logs/observability/error.log` | Daily | 90 days |
| Audit Log | `logs/observability/audit.log` | Daily | 365 days |

### Viewing Logs

#### Real-time Log Monitoring

```bash
# Follow main application log
tail -f logs/observability/app.log

# Follow with highlighting
tail -f logs/observability/app.log | grep --color -E 'ERROR|WARNING|$'

# Multiple log files
multitail logs/observability/app.log logs/observability/error.log
```

#### Searching Logs

```bash
# Find errors in last hour
grep "ERROR" logs/observability/app.log | awk -v date="$(date -d '1 hour ago' '+%Y-%m-%d %H')" '$0 ~ date'

# Search for specific document processing
grep "document_id=12345" logs/observability/app.log

# Find LLM API timeouts
grep -r "timeout" logs/llm_api/

# Count errors by type
grep "ERROR" logs/observability/app.log | awk -F':' '{print $NF}' | sort | uniq -c | sort -rn
```

#### Log Analysis

```bash
# Generate error summary
cat logs/observability/app.log | grep ERROR | \
    awk '{print $NF}' | sort | uniq -c | sort -rn > /tmp/error_summary.txt

# Processing time analysis
grep "processing_time" logs/observability/app.log | \
    awk -F'=' '{print $2}' | \
    awk '{sum+=$1; count++} END {print "Avg:", sum/count, "ms"}'
```

### Log Rotation

#### Manual Log Rotation

```bash
# Rotate logs manually
cd logs/observability
mv app.log app.log.$(date +%Y%m%d)
gzip app.log.$(date +%Y%m%d)
```

#### Logrotate Configuration

```
# /etc/logrotate.d/llm-document-enhancer
/path/to/llm-document-enhancer/logs/observability/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 appuser appgroup
    postrotate
        # Signal app to reopen log files if needed
        pkill -USR1 -f "run_pipeline.py" || true
    endscript
}
```

### Log Cleanup

```bash
# Clean logs older than 30 days
find logs/ -name "*.log" -mtime +30 -delete
find logs/ -name "*.log.gz" -mtime +90 -delete

# Clean old LLM response cache
find cache/llm_responses/ -mtime +7 -delete

# Archive important logs
tar -czvf logs_archive_$(date +%Y%m).tar.gz logs/observability/*.log.gz
```

---

## Scaling Procedures

### Vertical Scaling

#### Increase Memory Allocation

```bash
# Check current memory usage
ps aux | grep run_pipeline.py | awk '{print $4}'

# Run with increased memory limit
python -X dev scripts/run_pipeline.py
```

#### Optimize Python Settings

```bash
# Enable garbage collection tuning
export PYTHONMALLOC=malloc
export PYTHONHASHSEED=0

python scripts/run_pipeline.py
```

### Horizontal Scaling

#### Multiple Workers

```bash
# Start multiple pipeline workers
for i in {1..4}; do
    python scripts/run_pipeline.py --worker-id=$i &
done
```

#### Queue-Based Processing

```python
# Example: Distribute work across workers
from multiprocessing import Pool

def process_document(doc_path):
    # Process single document
    pass

with Pool(processes=4) as pool:
    pool.map(process_document, document_list)
```

### LLM API Rate Limiting

#### Configure Rate Limits

```python
# config/settings.py
LLM_CONFIG = {
    "rate_limit": 60,  # requests per minute
    "retry_attempts": 3,
    "retry_delay": 1.0,  # seconds
    "timeout": 30,  # seconds
}
```

#### Monitor Rate Limit Usage

```bash
# Check API call frequency
grep "LLM API call" logs/llm_api/*.log | \
    awk -F'T' '{print $1}' | uniq -c
```

---

## Backup and Recovery

### Backup Strategy

#### What to Backup

| Data Type | Frequency | Retention | Method |
|-----------|-----------|-----------|--------|
| Configuration | On change | Indefinite | Git |
| Outputs | Daily | 90 days | File copy |
| Cache | Weekly | 30 days | Archive |
| Logs | Daily | 30 days | Compress |

### Backup Procedures

#### Configuration Backup

```bash
# Backup all configuration
./scripts/backup_config.sh

# Or manually
mkdir -p backups/backup_$(date +%Y%m%d_%H%M%S)
cp -r config/ backups/backup_$(date +%Y%m%d_%H%M%S)/
```

#### Full Backup Script

```bash
#!/bin/bash
# backup.sh - Full backup procedure

BACKUP_DIR="backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup configuration
cp -r config/ "$BACKUP_DIR/"

# Backup outputs (last 7 days only)
find outputs/ -mtime -7 -type f -exec cp {} "$BACKUP_DIR/" \;

# Backup important logs
cp logs/observability/*.log "$BACKUP_DIR/"

# Compress backup
tar -czvf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup created: $BACKUP_DIR.tar.gz"
```

#### Automated Backups

```bash
# Add to crontab
# Daily backup at 2 AM
0 2 * * * /path/to/llm-document-enhancer/scripts/backup.sh

# Weekly cleanup of old backups
0 3 * * 0 find /path/to/backups/ -name "*.tar.gz" -mtime +30 -delete
```

### Recovery Procedures

#### Configuration Recovery

```bash
# List available backups
ls -la backups/

# Restore from specific backup
tar -xzvf backups/backup_20250530_020000.tar.gz

# Restore configuration
cp -r backup_20250530_020000/config/* config/
```

#### Full Recovery

```bash
#!/bin/bash
# restore.sh - Recovery procedure

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore.sh <backup_file.tar.gz>"
    exit 1
fi

# Stop service
pkill -f "run_pipeline.py"

# Extract backup
tar -xzvf "$BACKUP_FILE"

BACKUP_DIR=$(basename "$BACKUP_FILE" .tar.gz)

# Restore configuration
cp -r "$BACKUP_DIR/config/"* config/

# Restore outputs if needed
# cp -r "$BACKUP_DIR/outputs/"* outputs/

# Cleanup
rm -rf "$BACKUP_DIR"

echo "Recovery complete. Please restart the service."
```

---

## Deployment Procedures

### Pre-Deployment Checklist

- [ ] Backup current configuration
- [ ] Review changelog for breaking changes
- [ ] Test in staging environment
- [ ] Notify stakeholders
- [ ] Schedule maintenance window (if needed)

### Standard Deployment

#### Step 1: Prepare

```bash
# Create backup
./scripts/backup.sh

# Pull latest code
git fetch origin
git checkout main
git pull origin main
```

#### Step 2: Update Dependencies

```bash
# Update Python dependencies
pip install -r requirements.txt --upgrade

# Verify no conflicts
pip check
```

#### Step 3: Run Tests

```bash
# Run unit tests
python -m pytest tests_unit/ -v

# Run integration tests (optional in prod)
python -m pytest tests_integration/ -v --timeout=300
```

#### Step 4: Deploy

```bash
# Stop current service
pkill -f "run_pipeline.py"

# Apply database migrations (if any)
# python scripts/migrate.py

# Start service
python scripts/run_pipeline.py &
```

#### Step 5: Verify

```bash
# Health check
curl http://localhost:8080/health

# Smoke test
python scripts/smoke_test.py

# Monitor logs for errors
tail -f logs/observability/app.log
```

### Rollback Procedure

```bash
#!/bin/bash
# rollback.sh - Rollback to previous version

PREVIOUS_COMMIT=$1

if [ -z "$PREVIOUS_COMMIT" ]; then
    # Get previous commit
    PREVIOUS_COMMIT=$(git log --oneline -2 | tail -1 | awk '{print $1}')
fi

echo "Rolling back to $PREVIOUS_COMMIT"

# Stop service
pkill -f "run_pipeline.py"

# Rollback code
git checkout "$PREVIOUS_COMMIT"

# Restore dependencies
pip install -r requirements.txt

# Start service
python scripts/run_pipeline.py &

echo "Rollback complete"
```

---

## Emergency Procedures

### Incident Response

#### Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| P1 | Complete outage | < 15 min | Service crash, data loss |
| P2 | Major degradation | < 1 hour | High error rate, slow processing |
| P3 | Minor issue | < 4 hours | Single job failure, warnings |
| P4 | Low priority | < 24 hours | Cosmetic issues, minor bugs |

#### Incident Response Steps

1. **Acknowledge** - Confirm incident and assign owner
2. **Assess** - Determine severity and impact
3. **Mitigate** - Take immediate action to reduce impact
4. **Resolve** - Fix the root cause
5. **Review** - Post-incident review and documentation

### Emergency Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| On-Call Engineer | oncall@example.com | Slack #ops-alerts |
| Engineering Lead | lead@example.com | Phone |
| LLM Provider Support | support@openai.com | Ticket |

### Common Emergency Scenarios

#### Scenario: Service Completely Down

```bash
# 1. Check process status
pgrep -f "run_pipeline.py" || echo "Process not running"

# 2. Check recent logs
tail -100 logs/observability/error.log

# 3. Check disk space
df -h

# 4. Check memory
free -m

# 5. Restart service
python scripts/run_pipeline.py &

# 6. Verify recovery
curl http://localhost:8080/health
```

#### Scenario: High Error Rate

```bash
# 1. Check error patterns
grep ERROR logs/observability/app.log | tail -50

# 2. Check LLM API status
curl -s https://status.openai.com/api/v2/status.json | jq .

# 3. Check rate limit status
grep "rate_limit" logs/llm_api/*.log | tail -10

# 4. If rate limited, reduce concurrent requests
# Edit config/settings.py: rate_limit = 30
```

#### Scenario: Disk Space Full

```bash
# 1. Check disk usage
df -h
du -sh outputs/* | sort -rh | head -20

# 2. Clean old outputs
find outputs/ -mtime +30 -delete

# 3. Clean cache
rm -rf cache/llm_responses/*

# 4. Clean old logs
find logs/ -name "*.log" -mtime +7 -delete

# 5. Verify space recovered
df -h
```

#### Scenario: LLM API Errors

```bash
# 1. Check API key validity
curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"

# 2. Check provider status
# OpenAI: https://status.openai.com
# Anthropic: https://status.anthropic.com

# 3. Switch to fallback provider (if configured)
export LLM_PROVIDER="anthropic"

# 4. Restart service
pkill -f "run_pipeline.py" && python scripts/run_pipeline.py &
```

---

## Maintenance Windows

### Scheduled Maintenance

#### Weekly Maintenance (Sunday 2-4 AM)

- Log rotation
- Cache cleanup
- Backup verification
- Health check report

#### Monthly Maintenance (First Sunday 2-6 AM)

- Security patches
- Dependency updates
- Performance review
- Capacity planning

### Maintenance Procedures

#### Pre-Maintenance

```bash
# 1. Announce maintenance
# Post to Slack, send email

# 2. Stop accepting new work
# Drain queue or set maintenance flag

# 3. Wait for in-progress work to complete
watch 'pgrep -f "run_pipeline.py" | wc -l'

# 4. Create backup
./scripts/backup.sh
```

#### Post-Maintenance

```bash
# 1. Start service
python scripts/run_pipeline.py &

# 2. Health check
curl http://localhost:8080/health

# 3. Smoke test
python scripts/smoke_test.py

# 4. Monitor for 15 minutes
tail -f logs/observability/app.log

# 5. Announce completion
# Post to Slack, send email
```

---

## Appendix

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | None | Yes* |
| `ANTHROPIC_API_KEY` | Anthropic API key | None | Yes* |
| `LLM_PROVIDER` | LLM provider to use | `openai` | No |
| `LOG_LEVEL` | Logging verbosity | `INFO` | No |
| `CACHE_ENABLED` | Enable response cache | `true` | No |
| `CACHE_TTL` | Cache TTL in seconds | `3600` | No |
| `MAX_WORKERS` | Max concurrent workers | `4` | No |

*At least one API key is required

### Common Commands Reference

```bash
# Service Management
./run_desktop.command              # Start (interactive)
python scripts/run_pipeline.py &   # Start (background)
pkill -f "run_pipeline.py"         # Stop
pgrep -f "run_pipeline.py"         # Check status

# Health & Monitoring
curl http://localhost:8080/health  # Health check
tail -f logs/observability/app.log # View logs
grep ERROR logs/**/app.log         # Find errors

# Maintenance
./scripts/backup.sh                # Create backup
./scripts/restore.sh backup.tar.gz # Restore backup
pip install -r requirements.txt    # Update deps

# Troubleshooting
python scripts/run_pipeline.py --debug     # Debug mode
python -m pytest tests_unit/ -v            # Run tests
```

### File Permissions

```bash
# Recommended permissions
chmod 755 scripts/*.sh
chmod 644 config/*.json
chmod 600 .env  # API keys
chmod 755 outputs/
chmod 755 logs/
```

### Support Resources

- **Documentation:** `/docs/` directory
- **Troubleshooting Guide:** `docs/TROUBLESHOOTING.md`
- **Integration Guide:** `docs/INTEGRATION_GUIDE.md`
- **GitHub Issues:** [Repository Issues]
- **Slack:** #llm-document-enhancer

---

*Last reviewed: 2025-05-30*
