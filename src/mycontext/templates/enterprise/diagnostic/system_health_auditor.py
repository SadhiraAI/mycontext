"""
SystemHealthAuditor Pattern (Enterprise)

Comprehensive system health check across multiple dimensions.
Identify weaknesses before they become failures.

Research Foundation:
- Juran, J. M. (1988). Quality control handbook.
- ISO 9001 quality management systems.
- ITIL service management framework.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class SystemHealthAuditor(Pattern):
    """
    Comprehensive system health audit.

    Audit Dimensions:
    - Performance
    - Reliability
    - Security
    - Scalability
    - Maintainability
    - Compliance

    Use Cases:
    - System audits
    - Health checks
    - Preventive maintenance
    - Risk assessment

    Example:
        >>> from mycontext.templates.enterprise.diagnostic import SystemHealthAuditor
        >>>
        >>> pattern = SystemHealthAuditor()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     system="E-commerce web application",
        ...     audit_focus="Performance, security, scalability"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems auditor specializing in comprehensive health assessment. "
        "Evaluate system health across multiple critical dimensions.\n\n"
        "System: {system}\n"
        "Audit Focus: {audit_focus}\n\n"
        "Deliver your analysis:\n"
        "(1) Assess performance — response times, throughput, resource utilization vs. targets.\n"
        "(2) Evaluate reliability — uptime, error rates, mean time between failures and to recovery.\n"
        "(3) Check security — authentication, authorization, encryption, vulnerabilities.\n"
        "(4) Analyze scalability — current capacity, bottlenecks, horizontal and vertical scaling.\n"
        "(5) Review maintainability — technical debt, documentation, test coverage, deployment process.\n"
        "(6) Verify compliance — regulatory requirements and standards adherence.\n"
        "(7) Provide an overall health score with prioritized findings and a phased remediation roadmap.\n\n"
        "Be objective and risk-focused. Prioritize findings by severity and urgency.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="system_health_auditor",
            description="Comprehensive system health check",
            version="1.0.0",
            tags=["diagnostic", "enterprise", "audit", "health-check"],
            metadata={"category": "diagnostic", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Systems Auditor and Health Check Specialist",
                rules=[
                    "Audit across multiple dimensions systematically",
                    "Use objective metrics where possible",
                    "Identify issues before they become critical",
                    "Prioritize findings by severity and urgency",
                    "Provide actionable recommendations",
                ],
                style="thorough, objective, risk-focused, actionable",
            ),
            directive_template="""**SYSTEM HEALTH AUDIT**

**SYSTEM**: {system}

**AUDIT FOCUS**: {audit_focus}

---

## AUDIT DIMENSIONS

**Evaluate system health across key dimensions**:

### 1. PERFORMANCE

**Metrics**:
- Response time: [Current / Target / Status]
- Throughput: [Current / Target / Status]
- Resource utilization: [CPU, Memory, Disk, Network]

**Assessment**: ✅ Healthy / ⚠️ Warning / ❌ Critical

**Issues identified**:
- [Performance issue 1]
- [Performance issue 2]

**Recommendations**:
- [Fix 1]
- [Fix 2]

---

### 2. RELIABILITY

**Metrics**:
- Uptime: [%]
- Error rate: [Errors/hour]
- MTBF (Mean Time Between Failures): [Hours]
- MTTR (Mean Time To Recovery): [Minutes]

**Assessment**: ✅ / ⚠️ / ❌

**Issues**:
- [Reliability issue]

**Recommendations**:
- [Improvement]

---

### 3. SECURITY

**Checks**:
- Authentication: [Status]
- Authorization: [Status]
- Data encryption: [Status]
- Vulnerability scan: [Results]
- Access controls: [Status]

**Assessment**: ✅ / ⚠️ / ❌

**Vulnerabilities found**:
- [Security issue 1 - Severity: High/Medium/Low]
- [Security issue 2]

**Recommendations**:
- [Security fix 1 - Priority: Critical/High/Medium]
- [Security fix 2]

---

### 4. SCALABILITY

**Current capacity**:
- Max load handled: [Metrics]
- Bottlenecks: [Identified constraints]
- Horizontal scaling: [Possible/Limited/Not possible]
- Vertical scaling: [Status]

**Assessment**: ✅ / ⚠️ / ❌

**Scalability concerns**:
- [Limitation 1]

**Recommendations**:
- [Scaling strategy]

---

### 5. MAINTAINABILITY

**Code quality** (if applicable):
- Technical debt: [High/Medium/Low]
- Documentation: [Complete/Partial/Missing]
- Test coverage: [%]
- Code complexity: [Metrics]

**Operations**:
- Deployment process: [Manual/Automated/Status]
- Monitoring: [Comprehensive/Basic/None]
- Logging: [Quality]

**Assessment**: ✅ / ⚠️ / ❌

**Maintainability issues**:
- [Issue 1]

**Recommendations**:
- [Improvement 1]

---

### 6. COMPLIANCE

**Regulatory requirements**:
- [Regulation 1]: [Compliant/Non-compliant/Partial]
- [Regulation 2]: [Status]
- [Standard 1]: [Status]

**Assessment**: ✅ / ⚠️ / ❌

**Compliance gaps**:
- [Gap 1]

**Recommendations**:
- [Remediation 1]

---

## OVERALL HEALTH SCORE

**By dimension**:
| Dimension | Score | Status | Priority |
|-----------|-------|--------|----------|
| Performance | [X/10] | [Status] | [High/Med/Low] |
| Reliability | [X/10] | [Status] | [Priority] |
| Security | [X/10] | [Status] | [Priority] |
| Scalability | [X/10] | [Status] | [Priority] |
| Maintainability | [X/10] | [Status] | [Priority] |
| Compliance | [X/10] | [Status] | [Priority] |

**Overall**: [Y/10] - [Healthy / Needs Attention / Critical]

---

## CRITICAL FINDINGS

**Immediate attention required** (❌ Critical):
1. [Critical issue 1]
   - Impact: [High - could cause outage/breach/failure]
   - Urgency: [Fix within 24-48 hours]
   - Fix: [Immediate action]

---

## HIGH-PRIORITY FINDINGS

**Important but not emergency** (⚠️ Warning):
1. [Warning issue 1]
   - Impact: [Medium - degrades experience/risk]
   - Urgency: [Fix within 1-2 weeks]
   - Fix: [Planned action]

---

## MEDIUM-PRIORITY FINDINGS

**Should address** (⚠️ Advisory):
1. [Advisory issue 1]
   - Impact: [Low-Medium]
   - Urgency: [Fix within 1-3 months]
   - Fix: [Improvement plan]

---

## TRENDS ANALYSIS

**Health over time**:

**Improving**:
- [Metric that's getting better]
- [Another improvement]

**Stable**:
- [Metric holding steady]

**Degrading**:
- [Metric getting worse]
- [Area of concern]
- **Action needed**: [Intervention]

---

## RISK ASSESSMENT

**Likelihood vs. Impact matrix**:

| Finding | Likelihood | Impact | Risk Level | Priority |
|---------|------------|--------|------------|----------|
| [Issue 1] | High | High | Critical | 1 |
| [Issue 2] | High | Medium | High | 2 |
| [Issue 3] | Medium | High | High | 3 |
| [Issue 4] | Low | High | Medium | 4 |

---

## REMEDIATION ROADMAP

**Phased improvement plan**:

**Phase 1: Critical fixes** (Week 1):
1. [Critical fix 1]
2. [Critical fix 2]
- **Goal**: Eliminate immediate risks

**Phase 2: High-priority** (Weeks 2-4):
1. [Important fix 1]
2. [Important fix 2]
- **Goal**: Address major concerns

**Phase 3: Medium-priority** (Months 2-3):
1. [Improvement 1]
2. [Improvement 2]
- **Goal**: Optimize and harden

**Phase 4: Continuous improvement** (Ongoing):
- [Monitoring and optimization]

---

## MONITORING PLAN

**Ongoing health tracking**:

**Daily monitoring**:
- [Critical metric 1]
- [Critical metric 2]

**Weekly review**:
- [Performance trends]
- [Error rates]

**Monthly audit**:
- [Comprehensive health check]
- [Compare to baseline]

**Alerting**:
- If [metric] exceeds [threshold]: [Alert]
- Escalation: [Who to notify]

---

## PREVENTIVE MAINTENANCE

**Prevent future issues**:

**Regular maintenance**:
- [Task 1 - Frequency: Daily/Weekly/Monthly]
- [Task 2 - Frequency]

**Proactive measures**:
- [Prevention 1]
- [Prevention 2]

**Capacity planning**:
- Monitor growth trends
- Plan upgrades ahead of need

---

## AUDIT SUMMARY

**Executive summary** (for stakeholders):

**Overall health**: [Status]

**Critical actions**: [# items]

**Investment needed**: [Rough estimate]

**Timeline**: [Remediation duration]

**Risk if not addressed**: [Consequences]

**Recommended next steps**: [Priority actions]""",
            input_schema={"system": str, "audit_focus": str},
            constraints=Constraints(
                must_include=[
                    "multi_dimensional_audit",
                    "health_scores",
                    "prioritized_findings",
                    "remediation_plan",
                ],
                must_not_include=["superficial_check", "vague_findings"],
                style_guide="Systematic and thorough. Objective metrics. Prioritized by risk. Actionable recommendations.",
            ),
        )

    def build_context(self, system="", audit_focus="", **kwargs):
        """Build context for system health audit."""
        return super().build_context(system=system, audit_focus=audit_focus, **kwargs)

    def execute(self, provider="openai", system="", audit_focus="", **kwargs):
        """Execute system health audit."""
        return super().execute(provider=provider, system=system, audit_focus=audit_focus, **kwargs)


__all__ = ["SystemHealthAuditor"]
