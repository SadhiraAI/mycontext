# 🎯 Complete Pattern Guide - 50 Cognitive Patterns

**mycontext SDK - Universal Context Transformation Engine**

This comprehensive guide covers all 50 cognitive patterns, when to use them, how they make a difference, and real-world scenarios across industries and skill levels.

---

## 📚 Table of Contents

1. [Analysis Patterns (6)](#analysis-patterns)
2. [Reasoning Patterns (5)](#reasoning-patterns)
3. [Decision Patterns (5)](#decision-patterns)
4. [Creative Patterns (5)](#creative-patterns)
5. [Communication Patterns (7)](#communication-patterns)
6. [Planning Patterns (5)](#planning-patterns)
7. [Problem Solving Patterns (6)](#problem-solving-patterns)
8. [Specialized Patterns (11)](#specialized-patterns)
9. [Pattern Selection Guide](#pattern-selection-guide)
10. [Industry-Specific Use Cases](#industry-specific-use-cases)
11. [Role-Based Scenarios](#role-based-scenarios)

---

# Analysis Patterns

## 1. QuestionAnalyzer

### What It Does
Systematically breaks down questions to identify type, complexity, components, and optimal approach before attempting to answer.

### When to Use
- **Before answering any complex question**
- When questions are ambiguous or multi-layered
- When you need to understand question structure
- Before starting research or analysis

### How It Makes a Difference
**Without Pattern:** "How does blockchain work?" → Generic answer  
**With Pattern:** Identifies it's a concept explanation question requiring technical depth, practical examples, and security considerations

### Code Example

**Beginner:**
```python
from mycontext.templates.free.analysis import QuestionAnalyzer

analyzer = QuestionAnalyzer()
context = analyzer.build_context(
    question="What is machine learning?",
    depth="standard"
)

# Use with any LLM
openai_format = context.to_openai()
```

**Advanced:**
```python
analyzer = QuestionAnalyzer()
context = analyzer.build_context(
    question="How can we implement real-time fraud detection in our payment system?",
    depth="comprehensive",
    context_needed="Technical architecture, scalability requirements",
    domain="FinTech security"
)
```

### Industry Scenarios

**Healthcare:**
```python
question = "How do we improve patient readmission rates?"
# Pattern helps identify: metric optimization question, requires data analysis, 
# outcome measurement, and intervention strategies
```

**Finance:**
```python
question = "What factors affect stock price volatility?"
# Pattern identifies: causal relationship question, needs statistical analysis,
# historical data, and market context
```

**E-commerce:**
```python
question = "Why is cart abandonment increasing?"
# Pattern recognizes: diagnostic question, requires funnel analysis,
# user behavior data, and comparative timeframes
```

### Skill Level Examples

**Beginner Level:**
```python
# Simple product question
context = analyzer.build_context(
    question="What features should we add?",
    depth="basic"
)
```

**Intermediate Level:**
```python
# Business analysis
context = analyzer.build_context(
    question="How do our conversion rates compare to industry standards?",
    depth="detailed",
    context_needed="E-commerce, B2C SaaS"
)
```

**Advanced Level:**
```python
# Strategic planning
context = analyzer.build_context(
    question="What's the optimal pricing strategy for a multi-tier SaaS with usage-based components in emerging markets?",
    depth="comprehensive",
    context_needed="Competitive landscape, market maturity, customer segments",
    domain="SaaS pricing strategy"
)
```

---

## 2. DataAnalyzer

### What It Does
Structures systematic data analysis with pattern detection, insight extraction, and statistical rigor.

### When to Use
- Before analyzing any dataset
- When you need structured analysis approach
- For complex multi-dimensional data
- When presenting findings to stakeholders

### How It Makes a Difference
**Without Pattern:** "Analyze this sales data" → Random observations  
**With Pattern:** Structured analysis with hypothesis, methodology, statistical tests, visualizations, and actionable insights

### Code Example

**Beginner:**
```python
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()
context = analyzer.build_context(
    data_description="Monthly sales data (1 year)",
    analysis_goals=["Identify trends"],
    domain="Retail"
)
```

**Advanced:**
```python
context = analyzer.build_context(
    data_description="Customer behavior dataset: 500K users, 2M events, 50 features including demographics, activity logs, purchase history, support tickets",
    analysis_goals=[
        "Segment customers by lifetime value",
        "Predict churn probability",
        "Identify upsell opportunities",
        "Analyze feature usage patterns",
        "Calculate cohort retention"
    ],
    domain="B2B SaaS analytics",
    time_period="Last 18 months",
    key_metrics=["MRR, churn rate, NPS, product engagement score"]
)
```

### Industry Scenarios

**Healthcare:**
```python
context = analyzer.build_context(
    data_description="Patient outcomes data: 10K patients, treatment protocols, recovery times, readmission rates",
    analysis_goals=[
        "Identify factors affecting recovery time",
        "Compare treatment protocol effectiveness",
        "Predict readmission risk"
    ],
    domain="Hospital operations"
)
```

**Manufacturing:**
```python
context = analyzer.build_context(
    data_description="Production line sensor data: 1M readings, equipment performance, defect rates",
    analysis_goals=[
        "Predict equipment failures",
        "Optimize maintenance schedules",
        "Reduce defect rates"
    ],
    domain="Smart manufacturing"
)
```

**Marketing:**
```python
context = analyzer.build_context(
    data_description="Campaign performance: 50 campaigns, 2M impressions, conversion data, attribution tracking",
    analysis_goals=[
        "Calculate ROAS by channel",
        "Optimize budget allocation",
        "Identify high-performing segments"
    ],
    domain="Digital marketing"
)
```

---

## 3. TrendIdentifier

### What It Does
Detects patterns, trends, and anomalies in time-series or sequential data.

### When to Use
- Analyzing time-series data
- Monitoring metrics over time
- Forecasting future patterns
- Detecting anomalies or shifts

### How It Makes a Difference
**Without Pattern:** "Sales are up" → Vague observation  
**With Pattern:** "30% YoY growth, seasonal peaks in Q4, correlation with marketing spend, projected to reach $5M by year-end"

### Code Example

**Beginner:**
```python
from mycontext.templates.free.analysis import TrendIdentifier

identifier = TrendIdentifier()
context = identifier.build_context(
    data_description="Website traffic (6 months)",
    timeframe="Last 6 months",
    domain="Web analytics"
)
```

**Advanced:**
```python
context = identifier.build_context(
    data_description="Multi-channel revenue streams: organic search, paid ads, email, social, partnerships - daily granularity, 3 years historical",
    timeframe="36 months with daily granularity",
    domain="Growth analytics",
    metrics=["Revenue, CAC, LTV, conversion rate by channel"],
    external_factors=["Marketing campaigns, seasonality, economic indicators, competitor launches"]
)
```

### Real-World Scenarios

**Stock Market (Finance):**
```python
# Day trader scenario
context = identifier.build_context(
    data_description="Stock price movements for tech portfolio (10 stocks)",
    timeframe="Intraday, 5-minute intervals",
    domain="Quantitative trading"
)
```

**DevOps (Technology):**
```python
# SRE monitoring
context = identifier.build_context(
    data_description="API latency, error rates, CPU usage across 50 microservices",
    timeframe="Last 30 days, hourly aggregation",
    domain="Infrastructure monitoring",
    alert_conditions=["P95 latency > 500ms, error rate > 1%, CPU > 80%"]
)
```

---

## 4. GapAnalyzer

### What It Does
Identifies discrepancies between current state and desired state, highlighting what's missing or underperforming.

### When to Use
- Competitive analysis
- Process improvement
- Capability assessment
- Requirements gathering

### How It Makes a Difference
**Without Pattern:** "We need to improve" → Vague goal  
**With Pattern:** "Missing: API documentation (high priority), automated testing (critical), monitoring dashboard (medium priority)"

### Code Example

**Beginner:**
```python
from mycontext.templates.free.analysis import GapAnalyzer

analyzer = GapAnalyzer()
context = analyzer.build_context(
    current_state="Basic website with contact form",
    desired_state="Full e-commerce platform",
    domain="Web development"
)
```

**Advanced:**
```python
context = analyzer.build_context(
    current_state="Legacy monolith: PHP 7, MySQL, manual deployment, no testing, 10-minute deploys, 99.5% uptime",
    desired_state="Modern platform: microservices, containerized, CI/CD, 90% test coverage, sub-second deploys, 99.99% uptime, auto-scaling",
    domain="Platform engineering",
    constraints=["6-month migration window", "$500K budget", "Zero downtime requirement"],
    evaluation_criteria=["Technical feasibility", "Resource requirements", "Risk level", "Business impact"]
)
```

### Industry Examples

**Enterprise IT:**
```python
# Digital transformation
context = analyzer.build_context(
    current_state="On-premise servers, manual processes, email-based workflows, Excel reporting",
    desired_state="Cloud-native, automated workflows, integrated systems, real-time dashboards",
    domain="Enterprise IT modernization"
)
```

**Education:**
```python
# Curriculum development
context = analyzer.build_context(
    current_state="Traditional lectures, textbook-based, end-of-term exams",
    desired_state="Blended learning, interactive content, continuous assessment, personalized paths",
    domain="Educational technology"
)
```

---

## 5. SWOTAnalyzer

### What It Does
Structures analysis of Strengths, Weaknesses, Opportunities, and Threats for strategic planning.

### When to Use
- Strategic planning
- Business decisions
- Product launches
- Competitive positioning

### Code Example

```python
from mycontext.templates.free.analysis import SWOTAnalyzer

analyzer = SWOTAnalyzer()
context = analyzer.build_context(
    subject="Launching AI-powered customer service chatbot",
    domain="SaaS customer support",
    context_section="Mid-market B2B, 500 existing customers, 2 competitors with similar products"
)
```

### Business Scenario

**Startup Product Launch:**
```python
context = analyzer.build_context(
    subject="New mobile payment app in Southeast Asia market",
    domain="FinTech",
    context_section="""
    Market: 600M population, 60% smartphone penetration, growing digital payment adoption
    Competition: 3 major players (GrabPay, GoPay, local banks)
    Our advantage: Lower transaction fees, better UX
    Challenges: Regulatory compliance, user trust, network effects
    """
)
```

---

## 6. AnomalyDetector

### What It Does
Identifies unusual patterns, outliers, and deviations from expected behavior.

### When to Use
- Monitoring systems
- Fraud detection
- Quality control
- Security analysis

### Code Example

```python
from mycontext.templates.free.analysis import AnomalyDetector

detector = AnomalyDetector()
context = detector.build_context(
    data_description="Transaction patterns: 100K daily transactions, average $50-200",
    anomaly_type="Statistical outliers and behavioral anomalies",
    domain="Payment fraud detection"
)
```

### Critical Scenarios

**Cybersecurity:**
```python
context = detector.build_context(
    data_description="Network traffic: 10M packets/hour, typical patterns established",
    anomaly_type="Unusual traffic patterns, unexpected connections, data exfiltration attempts",
    domain="Network security"
)
```

**Manufacturing:**
```python
context = detector.build_context(
    data_description="Sensor readings from production line: temperature, pressure, vibration",
    anomaly_type="Equipment performance degradation, early failure indicators",
    domain="Predictive maintenance"
)
```

---

# Reasoning Patterns

## 7. StepByStepReasoner

### What It Does
Breaks down complex reasoning into logical, sequential steps with clear intermediate conclusions.

### When to Use
- Complex problem solving
- Teaching/explaining concepts
- Debugging logic
- Mathematical proofs

### How It Makes a Difference
**Without Pattern:** Jump to conclusion → Miss critical steps  
**With Pattern:** "Step 1: Identify inputs → Step 2: Apply formula → Step 3: Validate → Step 4: Interpret results"

### Code Example

**Beginner:**
```python
from mycontext.templates.free.reasoning import StepByStepReasoner

reasoner = StepByStepReasoner()
context = reasoner.build_context(
    problem="Calculate ROI for marketing campaign",
    goal="Determine if campaign was profitable"
)
```

**Advanced:**
```python
context = reasoner.build_context(
    problem="Design distributed caching strategy for global e-commerce platform serving 10M users across 5 continents",
    goal="Achieve <100ms latency globally while maintaining data consistency",
    domain="Distributed systems architecture",
    constraints=[
        "Must handle 50K requests/second",
        "Budget: $50K/month infrastructure",
        "Regulatory: GDPR, data residency requirements"
    ]
)
```

### Technical Scenarios

**Software Architecture:**
```python
# Microservices migration
context = reasoner.build_context(
    problem="Migrate monolithic order processing system to microservices",
    goal="Zero downtime migration with improved scalability",
    steps_needed=[
        "Identify service boundaries",
        "Design API contracts",
        "Implement strangler pattern",
        "Set up data synchronization",
        "Gradual traffic migration",
        "Decommission legacy components"
    ]
)
```

**Data Science:**
```python
# ML model deployment
context = reasoner.build_context(
    problem="Deploy churn prediction model to production",
    goal="Real-time predictions with monitoring and rollback capability",
    domain="MLOps"
)
```

---

## 8. AnalogicalReasoner

### What It Does
Uses analogies and comparisons to understand new concepts by relating them to familiar ones.

### When to Use
- Explaining complex concepts
- Finding creative solutions
- Cross-domain innovation
- Teaching new topics

### Code Example

```python
from mycontext.templates.free.reasoning import AnalogicalReasoner

reasoner = AnalogicalReasoner()
context = reasoner.build_context(
    new_concept="Kubernetes orchestration",
    familiar_concepts=["City traffic management", "Orchestra conductor"],
    domain="Container orchestration"
)
```

### Creative Applications

**Product Design:**
```python
# Designing new UX pattern
context = reasoner.build_context(
    new_concept="Real-time collaborative document editing",
    familiar_concepts=[
        "Google Docs collaboration",
        "Multiplayer video games",
        "Whiteboard brainstorming sessions"
    ],
    goal="Design intuitive conflict resolution UI"
)
```

**Business Model:**
```python
# New revenue model
context = reasoner.build_context(
    new_concept="Usage-based SaaS pricing",
    familiar_concepts=[
        "Utility billing (electricity, water)",
        "Pay-per-ride (Uber)",
        "AWS cloud pricing"
    ],
    domain="SaaS pricing strategy"
)
```

---

## 9. CausalReasoner

### What It Does
Identifies cause-and-effect relationships, distinguishing correlation from causation.

### When to Use
- Root cause analysis
- Impact assessment
- Hypothesis testing
- Scientific inquiry

### Code Example

```python
from mycontext.templates.free.reasoning import CausalReasoner

reasoner = CausalReasoner()
context = reasoner.build_context(
    effect="Website conversion rate dropped 15%",
    potential_causes=[
        "New checkout UI deployed",
        "Price increase",
        "Server performance issues",
        "Seasonal traffic patterns"
    ],
    domain="E-commerce optimization"
)
```

### Business Intelligence Scenarios

**Product Analytics:**
```python
context = reasoner.build_context(
    effect="User engagement increased 40% in cohort B",
    potential_causes=[
        "Onboarding tutorial changes",
        "Push notification strategy",
        "Feature discovery improvements",
        "Gamification elements"
    ],
    domain="Mobile app analytics",
    available_data="A/B test results, user surveys, session recordings"
)
```

---

## 10. RootCauseAnalyzer

### What It Does
Systematically drills down to find the underlying root causes of problems (5 Whys technique).

### When to Use
- Incident post-mortems
- Quality issues
- System failures
- Process breakdowns

### Code Example

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

analyzer = RootCauseAnalyzer()
context = analyzer.build_context(
    problem="Production API outage lasted 2 hours",
    impact="$500K revenue loss, 10K affected customers",
    domain="Site reliability engineering"
)
```

### DevOps Example

```python
# Post-mortem analysis
context = analyzer.build_context(
    problem="Database connection pool exhausted causing cascading failures",
    impact="Complete service outage, 3-hour downtime",
    domain="Infrastructure reliability",
    context_info="""
    Timeline: 2PM spike in traffic, connection pool maxed out at 2:15PM, 
    service degradation until 5PM recovery
    Contributing factors: No auto-scaling, inadequate monitoring, 
    missing circuit breakers
    """
)
```

---

## 11. HypothesisGenerator

### What It Does
Creates testable hypotheses based on observations, patterns, or questions.

### When to Use
- Scientific research
- A/B testing planning
- Exploratory analysis
- Innovation projects

### Code Example

```python
from mycontext.templates.free.reasoning import HypothesisGenerator

generator = HypothesisGenerator()
context = generator.build_context(
    observation="Mobile app users have 2x higher lifetime value than web users",
    domain="Product analytics",
    goal="Increase mobile adoption"
)
```

### Research Scenarios

**Growth Experiments:**
```python
context = generator.build_context(
    observation="Email open rates vary significantly by send time",
    domain="Email marketing",
    constraints=["Must be testable in 2 weeks", "Statistically significant sample size"],
    goal="Optimize send time strategy"
)
```

---

# Decision Patterns

## 12. DecisionFramework

### What It Does
Structures complex decisions with criteria, options, tradeoffs, and systematic evaluation.

### When to Use
- Major business decisions
- Technology choices
- Resource allocation
- Strategic planning

### How It Makes a Difference
**Without Pattern:** "Let's go with AWS" → Biased, unclear reasoning  
**With Pattern:** Systematic evaluation of 3 providers across 8 criteria with weighted scoring

### Code Example

**Beginner:**
```python
from mycontext.templates.free.decision import DecisionFramework

df = DecisionFramework()
context = df.build_context(
    decision="Choose project management tool",
    options=["Jira", "Asana", "Linear"],
    criteria=["Ease of use", "Price", "Integrations"]
)
```

**Advanced:**
```python
context = df.build_context(
    decision="Select cloud infrastructure provider for global expansion",
    options=["AWS", "Google Cloud", "Azure", "Multi-cloud hybrid"],
    criteria=[
        "Total cost of ownership (3-year)",
        "Global latency (P95 < 100ms)",
        "Service reliability (SLA 99.99%+)",
        "Team expertise and learning curve",
        "Vendor lock-in risk",
        "Compliance (GDPR, SOC2, HIPAA)",
        "AI/ML capabilities",
        "Support quality"
    ],
    constraints=[
        "Must support Kubernetes",
        "Budget: $500K first year, scaling to $2M",
        "Migration must complete in 6 months",
        "Zero downtime requirement"
    ],
    stakeholders=["CTO", "CFO", "DevOps team", "Security team"],
    decision_deadline="60 days",
    risk_tolerance="Low - business-critical infrastructure"
)
```

### Enterprise Scenarios

**Technology Stack Selection:**
```python
context = df.build_context(
    decision="Choose frontend framework for new product",
    options=["React", "Vue.js", "Angular", "Svelte"],
    criteria=[
        "Development velocity",
        "Talent availability",
        "Performance",
        "Ecosystem maturity",
        "Learning curve",
        "Long-term maintainability"
    ],
    constraints=["Team has 2 junior devs", "Must launch MVP in 3 months"],
    domain="Web application development"
)
```

**Vendor Selection:**
```python
context = df.build_context(
    decision="Select customer data platform (CDP)",
    options=["Segment", "mParticle", "Rudderstack", "Build in-house"],
    criteria=["Cost", "Integration ease", "Data quality", "Real-time capabilities", "Compliance"],
    constraints=["Must integrate with 15+ tools", "Budget: $100K/year"],
    domain="Marketing technology"
)
```

---

## 13. ComparativeAnalyzer

### What It Does
Detailed side-by-side comparison of multiple options across relevant dimensions.

### When to Use
- Evaluating alternatives
- Competitive analysis
- Feature comparison
- Benchmark studies

### Code Example

```python
from mycontext.templates.free.decision import ComparativeAnalyzer

analyzer = ComparativeAnalyzer()
context = analyzer.build_context(
    options=["PostgreSQL", "MongoDB", "DynamoDB"],
    criteria="Performance, Scalability, Cost, Query flexibility, Operations complexity",
    domain="Database selection"
)
```

### Product Comparison Scenarios

**API Design:**
```python
context = analyzer.build_context(
    options=["REST", "GraphQL", "gRPC"],
    criteria="""
    - Developer experience
    - Performance (latency, throughput)
    - Tooling and ecosystem
    - Learning curve
    - Mobile app suitability
    - Versioning and backwards compatibility
    """,
    domain="API architecture",
    use_case="Mobile-first social app with complex data relationships"
)
```

---

## 14. TradeoffAnalyzer

### What It Does
Explicitly identifies and evaluates tradeoffs between competing priorities or approaches.

### When to Use
- Architectural decisions
- Resource allocation
- Priority conflicts
- Technical debt discussions

### Code Example

```python
from mycontext.templates.free.decision import TradeoffAnalyzer

analyzer = TradeoffAnalyzer()
context = analyzer.build_context(
    option_a="Monolithic architecture",
    option_b="Microservices architecture",
    dimensions=["Development speed", "Scalability", "Operational complexity", "Team coordination", "Deployment flexibility"]
)
```

### Engineering Scenarios

**Technical Debt:**
```python
context = analyzer.build_context(
    option_a="Refactor legacy codebase (3 months)",
    option_b="Continue with quick fixes",
    dimensions=[
        "Short-term velocity",
        "Long-term maintainability",
        "Team morale",
        "Bug rate",
        "Onboarding time",
        "Feature development speed"
    ],
    domain="Software engineering management"
)
```

---

## 15. MultiObjectiveOptimizer

### What It Does
Optimizes decisions across multiple conflicting objectives simultaneously.

### When to Use
- Complex optimization problems
- Multi-stakeholder decisions
- Resource allocation
- Portfolio management

### Code Example

```python
from mycontext.templates.free.decision import MultiObjectiveOptimizer

optimizer = MultiObjectiveOptimizer()
context = optimizer.build_context(
    objectives=[
        "Maximize revenue",
        "Minimize customer churn",
        "Optimize resource utilization",
        "Maintain product quality"
    ],
    constraints=["Budget: $1M", "Timeline: 6 months", "Team size: 10 engineers"],
    domain="Product roadmap planning"
)
```

### Business Strategy Example

```python
context = optimizer.build_context(
    objectives=[
        "Maximize profit margins (target: 40%)",
        "Increase market share (target: +5%)",
        "Improve customer satisfaction (NPS >50)",
        "Reduce operational costs (target: -15%)"
    ],
    constraints=[
        "Cannot increase prices >10%",
        "Must maintain product quality",
        "Regulatory compliance required"
    ],
    domain="Strategic business planning",
    timeframe="12-month planning cycle"
)
```

---

## 16. CostBenefitAnalyzer

### What It Does
Systematic evaluation of costs vs benefits for investment decisions.

### When to Use
- Investment decisions
- Project prioritization
- Budget allocation
- ROI analysis

### Code Example

```python
from mycontext.templates.free.decision import CostBenefitAnalyzer

analyzer = CostBenefitAnalyzer()
context = analyzer.build_context(
    initiative="Implement automated testing",
    costs=["$50K initial setup", "2 engineers for 2 months", "CI/CD infrastructure"],
    benefits=["Reduce bugs 60%", "Faster releases", "Better developer experience"],
    timeframe="2-year analysis",
    domain="Software quality"
)
```

---

# Creative Patterns

## 17. IdeaGenerator

### What It Does
Generates creative ideas and solutions using structured brainstorming techniques.

### When to Use
- Product ideation
- Problem solving
- Innovation projects
- Marketing campaigns

### Code Example

**Beginner:**
```python
from mycontext.templates.free.creative import IdeaGenerator

generator = IdeaGenerator()
context = generator.build_context(
    challenge="Increase user engagement",
    constraints=["Limited budget", "2-month timeline"]
)
```

**Advanced:**
```python
context = generator.build_context(
    challenge="Create viral social media campaign for eco-friendly product launch",
    constraints=[
        "Budget: $50K",
        "Target: Gen Z and Millennials",
        "Must align with sustainability values",
        "Launch in 6 weeks"
    ],
    inspiration="Successful campaigns: Dove Real Beauty, Old Spice, Dollar Shave Club",
    desired_outcomes=[
        "1M+ social media impressions",
        "10K+ website visits",
        "Positive brand sentiment"
    ],
    domain="Digital marketing"
)
```

### Startup Scenarios

**Product Features:**
```python
context = generator.build_context(
    challenge="Differentiate our project management tool from 50+ competitors",
    constraints=["Small team (5 engineers)", "Must launch in 3 months"],
    inspiration="Notion's flexibility, Linear's speed, Figma's collaboration",
    target_audience="Remote-first startups, 10-50 employees"
)
```

---

## 18. Brainstormer

### What It Does
Facilitates divergent thinking to generate many ideas without judgment.

### When to Use
- Early ideation phases
- Problem exploration
- Creative workshops
- Innovation sessions

### Code Example

```python
from mycontext.templates.free.creative import Brainstormer

brainstormer = Brainstormer()
context = brainstormer.build_context(
    topic="Ways to reduce customer support tickets",
    constraints=["No additional budget for first 3 months"],
    goal="Reduce ticket volume by 30%"
)
```

### Team Workshop Example

```python
context = brainstormer.build_context(
    topic="Innovative ways to onboard remote employees",
    constraints=[
        "Fully remote team across 10 countries",
        "Mix of junior and senior hires",
        "Must be engaging and effective"
    ],
    goal="Create memorable, effective onboarding experience",
    participants="HR team, engineering managers, culture committee"
)
```

---

## 19. InnovationFramework

### What It Does
Structures innovation process from ideation through validation and execution.

### When to Use
- New product development
- Process innovation
- Business model innovation
- R&D projects

### Code Example

```python
from mycontext.templates.free.creative import InnovationFramework

framework = InnovationFramework()
context = framework.build_context(
    innovation_goal="Disrupt traditional banking with DeFi",
    domain="Financial technology",
    constraints=["Regulatory compliance", "User trust", "Technical complexity"],
    stage="Ideation"
)
```

---

## 20. DesignThinker

### What It Does
Applies design thinking methodology (empathize, define, ideate, prototype, test).

### When to Use
- User-centered design
- Product development
- Service design
- Customer experience

### Code Example

```python
from mycontext.templates.free.creative import DesignThinker

thinker = DesignThinker()
context = thinker.build_context(
    problem="Users abandon signup flow at payment step",
    user_needs=["Security", "Simplicity", "Transparency"],
    constraints=["Cannot remove payment step", "Must comply with PCI DSS"],
    domain="UX design"
)
```

---

## 21. MetaphorGenerator

### What It Does
Creates powerful metaphors and analogies to explain complex concepts.

### When to Use
- Technical writing
- Presentations
- Teaching
- Marketing copy

### Code Example

```python
from mycontext.templates.free.creative import MetaphorGenerator

generator = MetaphorGenerator()
context = generator.build_context(
    concept="Microservices architecture",
    target_audience="Non-technical executives",
    domain="Software architecture"
)
```

---

# Communication Patterns

## 22. SimplificationEngine

### What It Does
Simplifies complex concepts without losing essential meaning.

### When to Use
- Technical documentation
- Customer communication
- Executive summaries
- Educational content

### Code Example

**Beginner:**
```python
from mycontext.templates.free.communication import SimplificationEngine

engine = SimplificationEngine()
context = engine.build_context(
    complex_content="Blockchain consensus mechanisms",
    target_audience="General public",
    goal="Explain in simple terms"
)
```

**Advanced:**
```python
context = engine.build_context(
    complex_content="""
    Distributed consensus in blockchain networks using Proof-of-Work (PoW) 
    and Proof-of-Stake (PoS) mechanisms, including Byzantine Fault Tolerance,
    state machine replication, and economic incentive structures
    """,
    target_audience="Business executives with no technical background",
    goal="Explain for board presentation on blockchain investment",
    constraints=["5-minute presentation", "Focus on business implications"],
    tone="Professional but accessible"
)
```

### Documentation Scenarios

**API Documentation:**
```python
context = engine.build_context(
    complex_content="OAuth 2.0 authorization flow with PKCE extension",
    target_audience="Junior developers new to authentication",
    goal="Create beginner-friendly guide",
    domain="API documentation"
)
```

**User Guides:**
```python
context = engine.build_context(
    complex_content="Advanced Excel pivot table features and DAX formulas",
    target_audience="Business analysts with basic Excel knowledge",
    goal="Enable self-service data analysis"
)
```

---

## 23. ClarityOptimizer

### What It Does
Improves clarity, removes ambiguity, and enhances precision in communication.

### When to Use
- Contract review
- Requirements documents
- Policy writing
- Legal communications

### Code Example

```python
from mycontext.templates.free.communication import ClarityOptimizer

optimizer = ClarityOptimizer()
context = optimizer.build_context(
    content="Service Level Agreement terms",
    issues=["Vague uptime commitments", "Unclear response times"],
    domain="Legal/SLA"
)
```

---

## 24. AudienceAdapter

### What It Does
Adapts messaging and content for different audience types and contexts.

### When to Use
- Multi-stakeholder communication
- Marketing content
- Presentations
- Product positioning

### Code Example

```python
from mycontext.templates.free.communication import AudienceAdapter

adapter = AudienceAdapter()
context = adapter.build_context(
    core_message="Our ML model improves fraud detection by 40%",
    target_audiences=[
        "Technical team (data scientists)",
        "Business stakeholders (executives)",
        "Customers (non-technical users)"
    ],
    domain="Product communication"
)
```

### Multi-Stakeholder Example

```python
context = adapter.build_context(
    core_message="Implementing zero-trust security architecture",
    target_audiences=[
        "Board of Directors: Focus on risk reduction and compliance",
        "Engineering team: Focus on implementation details",
        "End users: Focus on what changes for them",
        "Legal/Compliance: Focus on regulatory implications"
    ],
    domain="Cybersecurity initiative"
)
```

---

## 25. PersuasionFramework

### What It Does
Structures persuasive arguments using proven rhetorical techniques.

### When to Use
- Sales pitches
- Proposals
- Negotiations
- Change management

### Code Example

```python
from mycontext.templates.free.communication import PersuasionFramework

framework = PersuasionFramework()
context = framework.build_context(
    goal="Convince board to approve $2M AI investment",
    audience="Risk-averse board members",
    key_points=["ROI projections", "Competitive necessity", "Pilot results"],
    objections=["High cost", "Unproven technology", "Implementation risk"]
)
```

---

## 26. NarrativeBuilder

### What It Does
Constructs compelling narratives with story arc, tension, and resolution.

### When to Use
- Brand storytelling
- Case studies
- Product launches
- Company culture

### Code Example

```python
from mycontext.templates.free.communication import NarrativeBuilder

builder = NarrativeBuilder()
context = builder.build_context(
    topic="Company transformation from near-bankruptcy to $100M valuation",
    audience="Investors and potential employees",
    narrative_goal="Inspire confidence and attract talent",
    key_moments=["Crisis point", "Pivot decision", "First big win", "Scale phase"]
)
```

---

## 27. TechnicalTranslator

### What It Does
Translates between technical and business language bidirectionally.

### When to Use
- Requirements gathering
- Technical proposals
- Cross-team communication
- Vendor discussions

### Code Example

```python
from mycontext.templates.free.communication import TechnicalTranslator

translator = TechnicalTranslator()
context = translator.build_context(
    source_language="Technical (engineering)",
    target_language="Business (executives)",
    content="We need to refactor the monolith into microservices for better scalability",
    domain="Software architecture"
)
```

---

## 28. FeedbackComposer

### What It Does
Structures constructive feedback using proven frameworks (SBI, sandwich method, etc.).

### When to Use
- Performance reviews
- Code reviews
- Design critiques
- Team feedback

### Code Example

```python
from mycontext.templates.free.communication import FeedbackComposer

composer = FeedbackComposer()
context = composer.build_context(
    feedback_topic="Code review - performance issues",
    recipient_level="Junior developer",
    tone="Constructive and encouraging",
    goal="Improve code quality while maintaining motivation"
)
```

---

# Planning Patterns

## 29. ScenarioPlanner

### What It Does
Creates multiple future scenarios (best/expected/worst case) for planning under uncertainty.

### When to Use
- Strategic planning
- Risk management
- Contingency planning
- Investment decisions

### Code Example

**Beginner:**
```python
from mycontext.templates.free.planning import ScenarioPlanner

planner = ScenarioPlanner()
context = planner.build_context(
    situation="Product launch",
    timeframe="First 6 months",
    scenarios=["Best case", "Expected", "Worst case"]
)
```

**Advanced:**
```python
context = planner.build_context(
    situation="International expansion into Asian markets",
    timeframe="3-year planning horizon",
    scenarios=[
        "Optimistic: Rapid adoption, favorable regulations, strong partnerships",
        "Baseline: Moderate growth, some regulatory hurdles, mixed market reception",
        "Pessimistic: Slow adoption, regulatory blocks, strong local competition",
        "Black swan: Geopolitical crisis affecting trade"
    ],
    key_variables=[
        "Regulatory environment",
        "Market adoption rate",
        "Competitive response",
        "Currency fluctuations",
        "Local partnership success"
    ],
    domain="International business development"
)
```

### Business Planning

**Fundraising:**
```python
context = planner.build_context(
    situation="Series A fundraising round",
    timeframe="12-month runway",
    scenarios=[
        "Oversubscribed round at higher valuation",
        "Standard round at target valuation",
        "Difficult raise at lower valuation",
        "Unable to raise, need bridge funding"
    ],
    contingency_plans_needed=True
)
```

---

## 30. StakeholderMapper

### What It Does
Identifies and analyzes all stakeholders, their interests, influence, and impact.

### When to Use
- Project kickoff
- Change initiatives
- Political navigation
- Communication planning

### Code Example

```python
from mycontext.templates.free.planning import StakeholderMapper

mapper = StakeholderMapper()
context = mapper.build_context(
    project="Implement new CRM system",
    organization_context="500-person company, sales-driven culture",
    domain="Change management"
)
```

### Enterprise Project Example

```python
context = mapper.build_context(
    project="Digital transformation initiative",
    organization_context="""
    5000 employees across 10 countries
    Traditional industry undergoing disruption
    Mix of tech-savvy and technology-resistant staff
    Multiple business units with different needs
    """,
    key_considerations=[
        "Identify champions and blockers",
        "Map influence networks",
        "Plan communication strategy",
        "Address concerns by stakeholder group"
    ]
)
```

---

## 31. PrioritySetter

### What It Does
Systematically prioritizes tasks, features, or initiatives using frameworks (RICE, MoSCoW, etc.).

### When to Use
- Roadmap planning
- Backlog grooming
- Resource allocation
- Sprint planning

### Code Example

**Beginner:**
```python
from mycontext.templates.free.planning import PrioritySetter

setter = PrioritySetter()
context = setter.build_context(
    items=["Feature A", "Bug fix B", "Tech debt C"],
    goal="Maximize user satisfaction",
    constraints=["2-week sprint", "3 developers"]
)
```

**Advanced (Product Roadmap):**
```python
context = setter.build_context(
    items=[
        "Mobile app v2.0 (major redesign)",
        "API v2 migration",
        "Enterprise SSO",
        "Advanced analytics dashboard",
        "Performance optimization",
        "Internationalization (5 languages)",
        "White-label capabilities",
        "Offline mode"
    ],
    goal="Maximize revenue impact while maintaining product quality",
    constraints=[
        "Engineering team: 12 devs",
        "Timeline: 6 months",
        "Must address top 3 enterprise customer requests",
        "Cannot compromise security or stability"
    ],
    prioritization_criteria=[
        "Revenue impact (enterprise vs SMB)",
        "Engineering effort (t-shirt sizing)",
        "Strategic value (competitive positioning)",
        "Customer demand (feature requests)",
        "Technical dependency (blockers)",
        "Risk level"
    ],
    framework="RICE scoring with custom weights",
    domain="SaaS product management"
)
```

---

## 32. DeadlineManager

### What It Does
Plans realistic timelines with dependencies, buffers, and risk mitigation.

### When to Use
- Project planning
- Launch coordination
- Deadline setting
- Time management

### Code Example

```python
from mycontext.templates.free.planning import DeadlineManager

manager = DeadlineManager()
context = manager.build_context(
    project="Launch new product",
    deadline="Q2 2026",
    key_milestones=["Design complete", "Development", "Testing", "Marketing"],
    risks=["Scope creep", "Resource constraints", "Dependencies"],
    domain="Project management"
)
```

---

## 33. ResourceAllocator

### What It Does
Optimizes allocation of limited resources (people, budget, time) across competing needs.

### When to Use
- Budget planning
- Team assignments
- Capacity planning
- Portfolio management

### Code Example

```python
from mycontext.templates.free.planning import ResourceAllocator

allocator = ResourceAllocator()
context = allocator.build_context(
    resources=["10 engineers", "$500K budget", "6 months"],
    competing_needs=[
        "New feature development",
        "Technical debt",
        "Bug fixes",
        "Infrastructure improvements"
    ],
    goal="Maximize business value while maintaining product health",
    domain="Engineering management"
)
```

---

# Problem Solving Patterns

## 34. ProblemDecomposer

### What It Does
Breaks complex problems into smaller, manageable sub-problems.

### When to Use
- Complex system design
- Large-scale projects
- Technical challenges
- Strategic initiatives

### Code Example

**Beginner:**
```python
from mycontext.templates.free.problem_solving import ProblemDecomposer

decomposer = ProblemDecomposer()
context = decomposer.build_context(
    problem="Build e-commerce website",
    context="Small business, first online presence"
)
```

**Advanced:**
```python
context = decomposer.build_context(
    problem="Scale application from 1K to 1M users while maintaining <100ms latency",
    context="""
    Current state:
    - Monolithic Rails app on single server
    - PostgreSQL database
    - Simple caching with Redis
    - 1K daily active users
    - Average response time: 200ms
    
    Target state:
    - 1M daily active users
    - P95 latency < 100ms
    - 99.95% uptime
    - Global distribution
    """,
    constraints=[
        "6-month timeline",
        "Cannot rewrite from scratch",
        "Zero downtime migration",
        "Team of 8 engineers"
    ],
    domain="Scalability engineering"
)
```

### System Design Example

```python
context = decomposer.build_context(
    problem="Design real-time collaborative document editing system (like Google Docs)",
    context="Support 50+ simultaneous editors per document",
    key_challenges=[
        "Conflict resolution",
        "Real-time synchronization",
        "Offline editing",
        "Performance at scale",
        "Data consistency"
    ],
    domain="Distributed systems design"
)
```

---

## 35. BottleneckIdentifier

### What It Does
Identifies performance bottlenecks, constraints, and limiting factors.

### When to Use
- Performance optimization
- Process improvement
- Capacity planning
- Efficiency analysis

### Code Example

```python
from mycontext.templates.free.problem_solving import BottleneckIdentifier

identifier = BottleneckIdentifier()
context = identifier.build_context(
    system="Order processing pipeline",
    performance_issues=["Slow checkout", "High abandonment"],
    current_metrics=["1000 orders/day", "15-second average checkout time"],
    domain="E-commerce operations"
)
```

### DevOps Example

```python
context = identifier.build_context(
    system="CI/CD pipeline",
    performance_issues=[
        "Deploy takes 45 minutes",
        "Tests are flaky",
        "Builds queue during peak hours"
    ],
    current_metrics=[
        "50 builds per day",
        "Test suite: 2000 tests, 30 minutes",
        "Average queue time: 15 minutes"
    ],
    goal="Reduce deploy time to <10 minutes",
    domain="DevOps optimization"
)
```

---

## 36. ConstraintOptimizer

### What It Does
Finds optimal solutions within given constraints and limitations.

### When to Use
- Resource optimization
- Budget planning
- Scheduling
- Design optimization

### Code Example

```python
from mycontext.templates.free.problem_solving import ConstraintOptimizer

optimizer = ConstraintOptimizer()
context = optimizer.build_context(
    problem="Maximize feature delivery",
    constraints=[
        "Budget: $100K",
        "Team: 5 developers",
        "Timeline: 3 months",
        "Must include security audit"
    ],
    optimization_goal="Maximize customer value while meeting compliance",
    domain="Product development"
)
```

---

## 37. DependencyMapper

### What It Does
Maps dependencies between components, tasks, or systems.

### When to Use
- Project planning
- System architecture
- Risk analysis
- Migration planning

### Code Example

```python
from mycontext.templates.free.problem_solving import DependencyMapper

mapper = DependencyMapper()
context = mapper.build_context(
    system="Microservices migration",
    components=[
        "User service",
        "Payment service",
        "Notification service",
        "Order service",
        "Inventory service"
    ],
    goal="Plan migration order to minimize risk",
    domain="System architecture"
)
```

---

## 38. EfficiencyAnalyzer

### What It Does
Analyzes processes or systems for efficiency improvements and waste reduction.

### When to Use
- Process optimization
- Cost reduction
- Productivity improvement
- Lean methodology

### Code Example

```python
from mycontext.templates.free.problem_solving import EfficiencyAnalyzer

analyzer = EfficiencyAnalyzer()
context = analyzer.build_context(
    process="Customer onboarding",
    current_state="Takes 5 days, 8 manual steps, 3 departments",
    goal="Reduce to 1 day",
    domain="Business process optimization"
)
```

---

## 39. TradeSpaceExplorer

### What It Does
Explores solution space to find optimal balance between competing objectives.

### When to Use
- Multi-objective optimization
- Design exploration
- Trade study analysis
- Requirements balancing

### Code Example

```python
from mycontext.templates.free.problem_solving import TradeSpaceExplorer

explorer = TradeSpaceExplorer()
context = explorer.build_context(
    objectives=["Performance", "Cost", "Maintainability"],
    constraints=["Must be production-ready in 3 months"],
    domain="Solution architecture"
)
```

---

# Specialized Patterns

## 40. CodeReviewer

### What It Does
Structures systematic code review focusing on security, performance, and best practices.

### When to Use
- Pull request reviews
- Security audits
- Code quality assessment
- Mentoring

### Code Example

```python
from mycontext.templates.free.specialized import CodeReviewer

reviewer = CodeReviewer()

code = """
def process_payment(amount, user_id):
    query = f"INSERT INTO payments VALUES ({amount}, {user_id})"
    db.execute(query)
    return True
"""

# Execute review (requires LLM provider)
# result = reviewer.execute(
#     provider="openai",
#     code=code,
#     language="Python",
#     context="Payment processing system",
#     focus_areas="Security, error handling, best practices"
# )
```

### Security Review Example

```python
# Security-focused review
context = reviewer.build_context(
    code=sensitive_code,
    language="Python",
    context="Authentication system handling user credentials",
    focus_areas="""
    - SQL injection vulnerabilities
    - Authentication bypass risks
    - Credential storage security
    - Input validation
    - Error handling and information disclosure
    """
)
```

---

## 41. ContentOutliner

### What It Does
Creates structured outlines for content, documentation, or presentations.

### When to Use
- Writing preparation
- Documentation planning
- Presentation design
- Course curriculum

### Code Example

```python
from mycontext.templates.free.specialized import ContentOutliner

outliner = ContentOutliner()
context = outliner.build_context(
    topic="Introduction to Machine Learning",
    audience="Software engineers new to ML",
    goal="Enable practical ML implementation",
    format="Workshop (3 hours)"
)
```

---

## 42. SocraticQuestioner

### What It Does
Uses Socratic method to explore topics through guided questioning.

### When to Use
- Teaching
- Requirements elicitation
- Problem exploration
- Critical thinking

### Code Example

```python
from mycontext.templates.free.specialized import SocraticQuestioner

questioner = SocraticQuestioner()
context = questioner.build_context(
    topic="Software design patterns",
    learning_goal="Understand when to use Singleton pattern",
    current_understanding="Basic OOP concepts"
)
```

---

## 43. IntentRecognizer

### What It Does
Identifies the underlying intent behind questions or requests.

### When to Use
- Customer support
- Requirements gathering
- User research
- Chatbot design

### Code Example

```python
from mycontext.templates.free.specialized import IntentRecognizer

recognizer = IntentRecognizer()
context = recognizer.build_context(
    user_input="The app keeps crashing when I try to upload photos",
    domain="Mobile app support",
    goal="Identify root issue and solution"
)
```

---

## 44. AmbiguityResolver

### What It Does
Identifies and resolves ambiguities in requirements, questions, or specifications.

### When to Use
- Requirements analysis
- Contract review
- Specification writing
- Communication clarification

### Code Example

```python
from mycontext.templates.free.specialized import AmbiguityResolver

resolver = AmbiguityResolver()
context = resolver.build_context(
    ambiguous_content="The system should be fast and handle lots of users",
    domain="Software requirements",
    goal="Create precise, testable requirements"
)
```

---

## 45. RiskAssessor

### What It Does
Systematic risk identification and assessment framework.

### When to Use
- Project planning
- Investment decisions
- Strategy development
- Compliance

### Code Example

```python
from mycontext.templates.free.specialized import RiskAssessor

assessor = RiskAssessor()
context = assessor.build_context(
    decision="Launch in new international market",
    context="FinTech product, heavily regulated",
    depth="comprehensive"
)
```

---

## 46. RiskMitigator

### What It Does
Develops strategies to mitigate identified risks.

### When to Use
- Risk management
- Contingency planning
- Disaster recovery
- Security planning

### Code Example

```python
from mycontext.templates.free.specialized import RiskMitigator

mitigator = RiskMitigator()
context = mitigator.build_context(
    risk="Data breach exposing customer information",
    impact="Severe - regulatory fines, reputation damage, customer loss",
    context="E-commerce platform with 500K users",
    depth="detailed"
)
```

---

## 47. ImpactAssessor

### What It Does
Evaluates the potential impact of decisions, changes, or events.

### When to Use
- Change management
- Feature planning
- Policy changes
- Business decisions

### Code Example

```python
from mycontext.templates.free.specialized import ImpactAssessor

assessor = ImpactAssessor()
context = assessor.build_context(
    action="Increase prices by 20%",
    context="B2B SaaS, 1000 customers, competitive market",
    stakeholders=["Existing customers", "Sales team", "New prospects"],
    depth="comprehensive"
)
```

---

## 48. ConflictResolver

### What It Does
Structures approach to resolving conflicts between stakeholders, requirements, or constraints.

### When to Use
- Negotiation
- Mediation
- Requirements conflicts
- Team disputes

### Code Example

```python
from mycontext.templates.free.specialized import ConflictResolver

resolver = ConflictResolver()
context = resolver.build_context(
    conflict="Engineering wants to refactor, Product wants new features",
    parties=["Engineering team", "Product team"],
    context="Startup under pressure to ship, technical debt accumulating",
    goal="Find win-win solution"
)
```

---

## 49. ConceptExplainer

### What It Does
Explains complex concepts using multiple teaching strategies.

### When to Use
- Technical writing
- Training materials
- Knowledge transfer
- Education

### Code Example

```python
from mycontext.templates.free.specialized import ConceptExplainer

explainer = ConceptExplainer()
context = explainer.build_context(
    concept="REST API authentication with JWT tokens",
    target_audience="Junior developers",
    teaching_approaches=["Analogy", "Example", "Step-by-step"],
    depth="detailed"
)
```

---

## 50. SynthesisBuilder

### What It Does
Synthesizes information from multiple sources into coherent understanding.

### When to Use
- Research synthesis
- Market analysis
- Literature review
- Competitive intelligence

### Code Example

```python
from mycontext.templates.free.specialized import SynthesisBuilder

builder = SynthesisBuilder()
context = builder.build_context(
    sources=[
        "Academic papers on ML bias",
        "Industry reports on AI ethics",
        "Case studies from major tech companies",
        "Regulatory guidelines"
    ],
    goal="Comprehensive understanding of AI bias mitigation",
    domain="AI ethics and governance"
)
```

---

# Pattern Selection Guide

## Quick Decision Tree

```
What's your goal?

├─ Understand a question better?
│  └─ Use: QuestionAnalyzer
│
├─ Analyze data?
│  ├─ Looking for trends? → TrendIdentifier
│  ├─ Comparing current vs desired? → GapAnalyzer
│  ├─ Finding anomalies? → AnomalyDetector
│  ├─ Strategic analysis? → SWOTAnalyzer
│  └─ General analysis? → DataAnalyzer
│
├─ Make a decision?
│  ├─ Comparing options? → ComparativeAnalyzer
│  ├─ Evaluating tradeoffs? → TradeoffAnalyzer
│  ├─ Multiple objectives? → MultiObjectiveOptimizer
│  ├─ Analyzing costs/benefits? → CostBenefitAnalyzer
│  └─ Complex decision? → DecisionFramework
│
├─ Solve a problem?
│  ├─ Complex problem? → ProblemDecomposer
│  ├─ Finding bottlenecks? → BottleneckIdentifier
│  ├─ Working with constraints? → ConstraintOptimizer
│  ├─ Mapping dependencies? → DependencyMapper
│  ├─ Improving efficiency? → EfficiencyAnalyzer
│  └─ Exploring solutions? → TradeSpaceExplorer
│
├─ Generate ideas?
│  ├─ Structured ideation? → IdeaGenerator
│  ├─ Free brainstorming? → Brainstormer
│  ├─ Innovation process? → InnovationFramework
│  ├─ User-centered design? → DesignThinker
│  └─ Creating analogies? → MetaphorGenerator
│
├─ Plan something?
│  ├─ Future scenarios? → ScenarioPlanner
│  ├─ Identifying stakeholders? → StakeholderMapper
│  ├─ Setting priorities? → PrioritySetter
│  ├─ Managing deadlines? → DeadlineManager
│  └─ Allocating resources? → ResourceAllocator
│
├─ Communicate?
│  ├─ Simplifying content? → SimplificationEngine
│  ├─ Improving clarity? → ClarityOptimizer
│  ├─ Adapting for audience? → AudienceAdapter
│  ├─ Being persuasive? → PersuasionFramework
│  ├─ Telling a story? → NarrativeBuilder
│  ├─ Translating tech↔business? → TechnicalTranslator
│  └─ Giving feedback? → FeedbackComposer
│
└─ Other specialized needs?
   ├─ Code review? → CodeReviewer
   ├─ Content outline? → ContentOutliner
   ├─ Socratic teaching? → SocraticQuestioner
   ├─ Recognizing intent? → IntentRecognizer
   ├─ Resolving ambiguity? → AmbiguityResolver
   ├─ Assessing risk? → RiskAssessor
   ├─ Mitigating risk? → RiskMitigator
   ├─ Impact analysis? → ImpactAssessor
   ├─ Resolving conflicts? → ConflictResolver
   ├─ Explaining concepts? → ConceptExplainer
   └─ Synthesizing information? → SynthesisBuilder
```

---

# Industry-Specific Use Cases

## Technology / Software

**Startup CTO Decision:**
```python
from mycontext.templates.free.decision import DecisionFramework

df = DecisionFramework()
context = df.build_context(
    decision="Choose tech stack for MVP",
    options=["MERN", "Next.js + Python", "Rails", "Django"],
    criteria=["Speed to market", "Developer availability", "Scalability", "Cost"],
    constraints=["3-month deadline", "2 developers", "$50K budget"]
)
```

**DevOps Optimization:**
```python
from mycontext.templates.free.problem_solving import BottleneckIdentifier

identifier = BottleneckIdentifier()
context = identifier.build_context(
    system="CI/CD pipeline",
    performance_issues=["45-minute deploys", "Flaky tests"],
    goal="Deploy in <10 minutes with 99% test reliability"
)
```

## Healthcare

**Clinical Trial Analysis:**
```python
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()
context = analyzer.build_context(
    data_description="Phase 2 trial results: 500 patients, 50 biomarkers, 6-month follow-up",
    analysis_goals=["Efficacy vs placebo", "Safety profile", "Subgroup analysis"],
    domain="Clinical research"
)
```

**Hospital Operations:**
```python
from mycontext.templates.free.problem_solving import EfficiencyAnalyzer

analyzer = EfficiencyAnalyzer()
context = analyzer.build_context(
    process="Emergency room patient flow",
    current_state="Average wait time: 4 hours, 30% capacity overflow",
    goal="Reduce wait time to <2 hours",
    domain="Healthcare operations"
)
```

## Finance

**Investment Decision:**
```python
from mycontext.templates.free.decision import CostBenefitAnalyzer

analyzer = CostBenefitAnalyzer()
context = analyzer.build_context(
    initiative="Acquire fintech startup",
    costs=["$50M acquisition", "Integration costs", "Regulatory compliance"],
    benefits=["New customer segment", "Technology capabilities", "Market share"],
    timeframe="5-year analysis",
    domain="M&A strategy"
)
```

**Risk Management:**
```python
from mycontext.templates.free.specialized import RiskAssessor

assessor = RiskAssessor()
context = assessor.build_context(
    decision="Launch cryptocurrency trading platform",
    context="Highly volatile market, regulatory uncertainty",
    depth="comprehensive"
)
```

## E-commerce / Retail

**Conversion Optimization:**
```python
from mycontext.templates.free.analysis import TrendIdentifier

identifier = TrendIdentifier()
context = identifier.build_context(
    data_description="Checkout funnel: page views, add-to-cart, checkout initiated, completed orders",
    timeframe="Last 12 months",
    domain="E-commerce analytics"
)
```

**Inventory Planning:**
```python
from mycontext.templates.free.planning import ScenarioPlanner

planner = ScenarioPlanner()
context = planner.build_context(
    situation="Holiday season inventory planning",
    timeframe="Q4 2026",
    scenarios=["High demand", "Average demand", "Economic downturn"],
    domain="Retail operations"
)
```

## Manufacturing

**Quality Control:**
```python
from mycontext.templates.free.analysis import AnomalyDetector

detector = AnomalyDetector()
context = detector.build_context(
    data_description="Production line sensor data: temperature, pressure, vibration",
    anomaly_type="Equipment degradation indicators",
    domain="Predictive maintenance"
)
```

**Process Optimization:**
```python
from mycontext.templates.free.problem_solving import ConstraintOptimizer

optimizer = ConstraintOptimizer()
context = optimizer.build_context(
    problem="Maximize production throughput",
    constraints=["Equipment capacity", "Labor hours", "Material supply", "Quality standards"],
    domain="Manufacturing optimization"
)
```

## Marketing / Advertising

**Campaign Planning:**
```python
from mycontext.templates.free.creative import IdeaGenerator

generator = IdeaGenerator()
context = generator.build_context(
    challenge="Launch campaign for eco-friendly product",
    constraints=["$100K budget", "Target: Millennials and Gen Z"],
    inspiration="Patagonia, TOMS, Seventh Generation campaigns"
)
```

**Performance Analysis:**
```python
from mycontext.templates.free.decision import MultiObjectiveOptimizer

optimizer = MultiObjectiveOptimizer()
context = optimizer.build_context(
    objectives=["Maximize ROI", "Increase brand awareness", "Generate qualified leads"],
    constraints=["$50K monthly budget", "Q2 goals"],
    domain="Digital marketing"
)
```

---

# Role-Based Scenarios

## Data Scientists

### Beginner Data Scientist

**First Data Analysis Project:**
```python
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()
context = analyzer.build_context(
    data_description="Customer dataset: 10K rows, demographics, purchase history",
    analysis_goals=["Find patterns", "Segment customers"],
    domain="Customer analytics"
)
```

### Advanced Data Scientist

**Complex ML Pipeline:**
```python
from mycontext.templates.free.problem_solving import ProblemDecomposer

decomposer = ProblemDecomposer()
context = decomposer.build_context(
    problem="Build real-time fraud detection system handling 10K transactions/second",
    context="""
    Requirements: <100ms latency, 99.9% accuracy, explainable predictions,
    A/B testing framework, continuous model retraining
    """,
    domain="ML systems engineering"
)
```

## Software Engineers

### Junior Engineer

**Code Review Learning:**
```python
from mycontext.templates.free.specialized import CodeReviewer

# Create context for understanding code review
context = reviewer.build_context(
    code=my_first_pull_request,
    language="Python",
    context="REST API endpoint",
    focus_areas="Best practices, error handling"
)
```

### Senior Engineer

**Architecture Decision:**
```python
from mycontext.templates.free.decision import TradeoffAnalyzer

analyzer = TradeoffAnalyzer()
context = analyzer.build_context(
    option_a="Microservices with Kubernetes",
    option_b="Serverless with AWS Lambda",
    dimensions=[
        "Operational complexity",
        "Cost at scale",
        "Development velocity",
        "Vendor lock-in risk",
        "Team expertise required"
    ],
    domain="Cloud architecture"
)
```

## Product Managers

### APM (Associate Product Manager)

**Feature Prioritization:**
```python
from mycontext.templates.free.planning import PrioritySetter

setter = PrioritySetter()
context = setter.build_context(
    items=["Dark mode", "Export PDF", "Mobile app", "API access"],
    goal="Maximize user satisfaction",
    constraints=["2-month timeline", "5 engineers"]
)
```

### Senior PM

**Strategic Roadmap:**
```python
from mycontext.templates.free.decision import MultiObjectiveOptimizer

optimizer = MultiObjectiveOptimizer()
context = optimizer.build_context(
    objectives=[
        "Increase revenue 30%",
        "Improve NPS >50",
        "Reduce churn <5%",
        "Launch in 2 new markets"
    ],
    constraints=["$5M budget", "Team of 50", "12-month timeframe"],
    domain="Product strategy"
)
```

## Business Analysts

### Junior Analyst

**Basic Analysis:**
```python
from mycontext.templates.free.analysis import TrendIdentifier

identifier = TrendIdentifier()
context = identifier.build_context(
    data_description="Monthly sales data (2 years)",
    timeframe="Last 24 months",
    domain="Sales analytics"
)
```

### Senior Analyst

**Strategic Analysis:**
```python
from mycontext.templates.free.analysis import SWOTAnalyzer

analyzer = SWOTAnalyzer()
context = analyzer.build_context(
    subject="Market entry strategy for Southeast Asia",
    domain="Strategic business analysis",
    context_section="B2B SaaS, $10M ARR, Series A funded"
)
```

## Marketing Managers

**Campaign Strategy:**
```python
from mycontext.templates.free.communication import AudienceAdapter

adapter = AudienceAdapter()
context = adapter.build_context(
    core_message="AI-powered analytics tool saves 10 hours/week",
    target_audiences=[
        "C-level: ROI focus",
        "Managers: Efficiency gains",
        "End users: Ease of use"
    ],
    domain="B2B marketing"
)
```

## Founders / CEOs

**Strategic Decision:**
```python
from mycontext.templates.free.decision import DecisionFramework

df = DecisionFramework()
context = df.build_context(
    decision="Raise Series A vs bootstrap to profitability",
    options=["Raise $5M Series A", "Cut costs, reach profitability in 12 months"],
    criteria=["Growth rate", "Control", "Risk", "Market timing", "Competitive position"],
    constraints=["18-month runway", "Strong unit economics"],
    domain="Startup strategy"
)
```

---

# Best Practices

## Pattern Selection

1. **Start Simple:** Begin with basic patterns before combining multiple patterns
2. **Match Complexity:** Use advanced parameters only when needed
3. **Iterate:** Measure quality, refine, repeat
4. **Combine:** Many real-world scenarios benefit from multiple patterns in sequence

## Quality Optimization

```python
from mycontext.intelligence import QualityMetrics

# Always measure your context quality
metrics = QualityMetrics()
score = metrics.evaluate(context)

# If quality < 0.7, enhance the context
if score.overall < 0.7:
    # Add more specifics, constraints, or use a different pattern
    pass
```

## Export Strategy

```python
# Choose export format based on use case
context.to_openai()      # For GPT-4 API
context.to_anthropic()   # For Claude API
context.to_langchain()   # For LangChain pipelines
context.to_yaml()        # For configuration/sharing
context.to_markdown()    # For documentation
```

---

# Conclusion

This guide covers all 50 cognitive patterns in the mycontext SDK. Each pattern is designed for specific use cases, but they can be combined and adapted for your unique needs.

**Remember:**
- Start with the pattern selection guide
- Use beginner examples to learn
- Scale to advanced patterns as needed
- Measure quality and iterate
- Combine patterns for complex scenarios

**Need help?** 
- Check the Jupyter notebooks in `examples/`
- Review API reference in README.md
- Join the community discussions

**Happy Context Engineering! 🚀**

---

**Last Updated:** February 2026  
**Version:** 0.2.0  
**For:** mycontext SDK - Universal Context Transformation Engine
