import sys
import os

# Add apps/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api")))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import (
    Track,
    Organization,
    User,
    Membership,
    Role,
    Profile,
    CompetencyFramework,
    Competency,
    RoleCompetency,
    UserCompetency,
    LearningResource,
    ResourceCompetency,
    Assessment,
    AssessmentQuestion,
    SkillGap,
    Recommendation,
    LearningPath,
    LearningPathItem,
    AuditEvent,
    CompetencyHistory,
)


def seed_database():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if already seeded
        existing_user = db.query(User).filter_by(email="ananya.rao@mospi.gov.in").first()
        if existing_user:
            print("Database already seeded with demo users. Skipping...")
            return

        print("Seeding Tracks...")
        track_gov = Track(code="GOVERNMENT", name="Government & Official Statistics")
        track_ind = Track(code="INDUSTRY", name="Industry & Professional Careers")
        track_acad = Track(code="ACADEMIA", name="Higher Education & Curriculum")
        db.add_all([track_gov, track_ind, track_acad])
        db.flush()

        print("Seeding Organizations...")
        org_mospi = Organization(
            name="Ministry of Statistics and Programme Implementation (MoSPI)",
            type="GOVERNMENT",
            metadata_json={"division": "DIID", "country": "India"}
        )
        org_nssta = Organization(
            name="National Statistical Systems Training Academy (NSSTA)",
            type="GOVERNMENT",
            metadata_json={"type": "Training Institute", "parent": "MoSPI"}
        )
        org_industry = Organization(
            name="Analytics & AI Enterprise Solutions",
            type="INDUSTRY",
            metadata_json={"sector": "Technology & Analytics"}
        )
        org_univ = Organization(
            name="National Institute of Science & Technology",
            type="ACADEMIA",
            metadata_json={"tier": "Higher Education"}
        )
        db.add_all([org_mospi, org_nssta, org_industry, org_univ])
        db.flush()

        print("Seeding Roles...")
        role_stat_officer = Role(
            track_id=track_gov.id,
            name="Statistical Officer",
            description="Responsible for national survey design, sampling implementation, data validation, and SDG indicator tracking.",
            organization_id=org_mospi.id
        )
        role_data_analyst = Role(
            track_id=track_ind.id,
            name="Data Analyst / BI Analyst",
            description="Analyzes complex business datasets, builds executive dashboards, writes SQL queries, and surfaces predictive insights.",
            organization_id=org_industry.id
        )
        role_student = Role(
            track_id=track_acad.id,
            name="B.E. Computer Science / Statistics Student",
            description="Undergraduate student building academic competencies, coursework projects, and preparing for industry internships.",
            organization_id=org_univ.id
        )
        db.add_all([role_stat_officer, role_data_analyst, role_student])
        db.flush()

        print("Seeding Competency Frameworks...")
        fw_gov = CompetencyFramework(
            track_id=track_gov.id,
            name="MoSPI Official Statistics Competency Framework",
            version="2026.1",
            status="active"
        )
        fw_ind = CompetencyFramework(
            track_id=track_ind.id,
            name="Industry Analytics & AI Competency Standard",
            version="2026.1",
            status="active"
        )
        fw_acad = CompetencyFramework(
            track_id=track_acad.id,
            name="Undergraduate Statistical & Computing Curriculum Framework",
            version="2026.1",
            status="active"
        )
        db.add_all([fw_gov, fw_ind, fw_acad])
        db.flush()

        print("Seeding Competencies for Government Framework...")
        gov_competencies_data = [
            # Statistical
            ("STAT-01", "Survey Design", "Statistical", "Methodology for planning, structuring, and launching national-scale census and sample surveys."),
            ("STAT-02", "Sampling Techniques", "Statistical", "Stratified, multi-stage, cluster, and probability proportional to size (PPS) sampling."),
            ("STAT-03", "National Accounts", "Statistical", "GDP calculation, Gross Value Added (GVA), and national macroeconomic accounting standards."),
            ("STAT-04", "Price Statistics", "Statistical", "Consumer Price Index (CPI), Wholesale Price Index (WPI), and inflation measurement."),
            ("STAT-05", "SDG Indicators", "Statistical", "Sustainable Development Goals monitoring, NIF alignment, and indicator aggregation."),
            ("STAT-06", "Data Quality Frameworks", "Statistical", "Statistical data quality assessment, accuracy, timeliness, and metadata documentation."),
            # Technical
            ("TECH-01", "Python for Analytics", "Technical", "Data manipulation with Pandas, NumPy, statistical modeling, and automation scripting."),
            ("TECH-02", "R for Official Statistics", "Technical", "Statistical computing, survey weighting, econometrics, and survey package usage."),
            ("TECH-03", "SQL & Database Queries", "Technical", "Relational database querying, aggregations, window functions, and indexing."),
            ("TECH-04", "GIS & Spatial Mapping", "Technical", "Geospatial data integration, shapefiles, choropleth maps, and census boundary mapping."),
            ("TECH-05", "Data Visualization", "Technical", "Visual analytics, interactive dashboards, chart selection, and executive storytelling."),
            # Digital Governance
            ("GOV-01", "Cybersecurity & Data Privacy", "Digital Governance", "IT security policies, data classification, anonymization, and DPDP Act compliance."),
            ("GOV-02", "Digital Public Infrastructure", "Digital Governance", "Government cloud, API gateways, digital signatures, and e-governance standards."),
            # Behavioural
            ("MGT-01", "Leadership & Ethics", "Behavioural / Managerial", "Ethical decision making, statistical integrity, conflict management, and public administration.")
        ]

        gov_competency_objects = {}
        for code, name, category, desc in gov_competencies_data:
            c = Competency(
                framework_id=fw_gov.id,
                code=code,
                name=name,
                category=category,
                description=desc,
                level_definitions_json={
                    "1": "Novice: Basic awareness of terminology",
                    "2": "Beginner: Can perform routine tasks with guidance",
                    "3": "Competent: Performs independent analysis and validation",
                    "4": "Proficient: Solves complex methodological problems",
                    "5": "Expert: Designs frameworks and mentors others"
                }
            )
            db.add(c)
            gov_competency_objects[code] = c

        print("Seeding Competencies for Industry Framework...")
        ind_competencies_data = [
            ("IND-SQL", "Advanced SQL & Warehousing", "Technical", "Complex queries, ETL optimization, star schemas, and analytical data marts."),
            ("IND-PY", "Python Data Engineering", "Technical", "Pipeline orchestration, Pandas, data cleaning, and REST API consumption."),
            ("IND-BI", "Business Intelligence & Power BI", "Analytics", "Executive dashboards, DAX expressions, KPI models, and business storytelling."),
            ("IND-ML", "Applied Machine Learning", "AI/ML", "Predictive modeling, scikit-learn, classification, regression, and model validation."),
            ("IND-GIT", "Version Control & Collaboration", "Engineering", "Git branching workflows, code reviews, documentation, and CI/CD basics.")
        ]

        ind_competency_objects = {}
        for code, name, category, desc in ind_competencies_data:
            c = Competency(
                framework_id=fw_ind.id,
                code=code,
                name=name,
                category=category,
                description=desc,
                level_definitions_json={
                    "1": "Awareness",
                    "2": "Basic Practitioner",
                    "3": "Independent Builder",
                    "4": "Senior Contributor",
                    "5": "Lead / Architect"
                }
            )
            db.add(c)
            ind_competency_objects[code] = c

        print("Seeding Competencies for Academia Framework...")
        acad_competencies_data = [
            ("ACAD-STAT", "Probability & Mathematical Statistics", "Academic Core", "Discrete and continuous distributions, hypothesis testing, and ANOVA."),
            ("ACAD-DBMS", "Database Management Systems", "Academic Core", "Relational algebra, normalization, transaction ACID properties, and SQL."),
            ("ACAD-PROG", "Object-Oriented Programming (Python)", "Academic Core", "Data structures, algorithms, modular programming, and debugging."),
            ("ACAD-VIZ", "Data Visualization & Exploration", "Academic Core", "Exploratory data analysis, statistical plotting, and metric interpretation.")
        ]

        acad_competency_objects = {}
        for code, name, category, desc in acad_competencies_data:
            c = Competency(
                framework_id=fw_acad.id,
                code=code,
                name=name,
                category=category,
                description=desc,
                level_definitions_json={
                    "1": "Course Theory Understood",
                    "2": "Lab Exercises Solved",
                    "3": "Course Project Implemented",
                    "4": "Research / Extension Ready",
                    "5": "Subject Mastery"
                }
            )
            db.add(c)
            acad_competency_objects[code] = c

        db.flush()

        print("Mapping Role Competencies for Statistical Officer...")
        role_comp_mappings = [
            (gov_competency_objects["STAT-01"].id, 4, 1.2, "CRITICAL"),
            (gov_competency_objects["STAT-02"].id, 4, 1.2, "CRITICAL"),
            (gov_competency_objects["STAT-03"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["STAT-04"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["STAT-05"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["STAT-06"].id, 4, 1.1, "CRITICAL"),
            (gov_competency_objects["TECH-01"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["TECH-02"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["TECH-03"].id, 3, 1.0, "HIGH"),
            (gov_competency_objects["TECH-04"].id, 3, 0.9, "MEDIUM"),
            (gov_competency_objects["TECH-05"].id, 3, 0.9, "MEDIUM"),
            (gov_competency_objects["GOV-01"].id, 3, 1.0, "HIGH"),
        ]
        for comp_id, req_lvl, weight, priority in role_comp_mappings:
            db.add(RoleCompetency(
                role_id=role_stat_officer.id,
                competency_id=comp_id,
                required_level=req_lvl,
                weight=weight,
                priority=priority
            ))

        print("Seeding Users & Profiles...")
        default_pwd = get_password_hash("DemoUser@123")
        admin_pwd = get_password_hash("AdminUser@123")

        # 1. Government Demo User: Ananya Rao
        user_ananya = User(
            email="ananya.rao@mospi.gov.in",
            display_name="Ananya Rao",
            password_hash=default_pwd,
            status="active"
        )
        db.add(user_ananya)
        db.flush()

        db.add(Membership(
            user_id=user_ananya.id,
            organization_id=org_mospi.id,
            role="official",
            status="active"
        ))

        db.add(Profile(
            user_id=user_ananya.id,
            track_id=track_gov.id,
            designation="Statistical Officer",
            department="State Statistics Department / DIID",
            experience_json={"years": 4, "surveys_handled": ["ASI", "PLFS"]},
            career_goal="Senior Director of Survey Methodology",
            target_role_id=role_stat_officer.id,
            metadata_json={"track": "GOVERNMENT", "state": "Karnataka"}
        ))

        # 2. Industry Demo User: Neha Sharma
        user_neha = User(
            email="neha.sharma@datatech.io",
            display_name="Neha Sharma",
            password_hash=default_pwd,
            status="active"
        )
        db.add(user_neha)
        db.flush()

        db.add(Membership(
            user_id=user_neha.id,
            organization_id=org_industry.id,
            role="professional",
            status="active"
        ))

        db.add(Profile(
            user_id=user_neha.id,
            track_id=track_ind.id,
            designation="Junior Data Analyst",
            department="Product Analytics",
            experience_json={"years": 1.5, "tools": ["Excel", "SQL"]},
            career_goal="Lead BI Analyst & Analytics Engineer",
            target_role_id=role_data_analyst.id,
            metadata_json={"track": "INDUSTRY"}
        ))

        # 3. Academia Demo User: Arjun Mehta
        user_arjun = User(
            email="arjun.mehta@univ.edu.in",
            display_name="Arjun Mehta",
            password_hash=default_pwd,
            status="active"
        )
        db.add(user_arjun)
        db.flush()

        db.add(Membership(
            user_id=user_arjun.id,
            organization_id=org_univ.id,
            role="student",
            status="active"
        ))

        db.add(Profile(
            user_id=user_arjun.id,
            track_id=track_acad.id,
            designation="Student",
            department="Department of Computer Science & Engineering",
            education_json={"degree": "B.E. Computer Science", "year": "3rd Year", "cgpa": 8.4},
            career_goal="Data Analyst / Machine Learning Engineer",
            target_role_id=role_student.id,
            metadata_json={"track": "ACADEMIA"}
        ))

        # 4. Admin User: Admin
        user_admin = User(
            email="admin@statskill.gov.in",
            display_name="System Administrator (MoSPI)",
            password_hash=admin_pwd,
            status="active"
        )
        db.add(user_admin)
        db.flush()

        db.add(Membership(
            user_id=user_admin.id,
            organization_id=org_mospi.id,
            role="platform_admin",
            status="active"
        ))

        print("Seeding Initial Competencies and Skill Gaps for Ananya Rao...")
        ananya_competencies = [
            ("STAT-01", 72.0, 3, 0.85, "diagnostic"),
            ("STAT-02", 55.0, 2, 0.80, "diagnostic"),
            ("STAT-03", 68.0, 3, 0.75, "diagnostic"),
            ("STAT-04", 45.0, 2, 0.70, "diagnostic"),
            ("STAT-05", 58.0, 2, 0.70, "diagnostic"),
            ("STAT-06", 80.0, 4, 0.90, "diagnostic"),
            ("TECH-01", 62.0, 3, 0.80, "diagnostic"),
            ("TECH-02", 35.0, 1, 0.65, "diagnostic"),
            ("TECH-03", 75.0, 3, 0.85, "diagnostic"),
            ("TECH-04", 40.0, 2, 0.60, "diagnostic"),
            ("TECH-05", 65.0, 3, 0.80, "diagnostic"),
            ("GOV-01", 50.0, 2, 0.75, "diagnostic"),
        ]

        for code, score, level, conf, src in ananya_competencies:
            comp = gov_competency_objects[code]
            db.add(UserCompetency(
                user_id=user_ananya.id,
                competency_id=comp.id,
                score=score,
                proficiency_level=level,
                confidence=conf,
                source=src
            ))
            # Calculate gap against required level (assuming target level 3 or 4)
            req_level = 4 if code in ["STAT-01", "STAT-02", "STAT-06"] else 3
            req_score = req_level * 20.0
            gap_val = max(0.0, req_score - score)
            priority = "CRITICAL" if gap_val >= 35.0 else ("HIGH" if gap_val >= 20.0 else "MEDIUM")
            status = "OPEN" if gap_val > 0 else "RESOLVED"
            db.add(SkillGap(
                user_id=user_ananya.id,
                competency_id=comp.id,
                required_level=req_level,
                current_score=score,
                gap_value=gap_val,
                priority=priority,
                status=status,
                explanation=f"Official target level is {req_level} ({req_score:.0f} pts). Current validated score is {score:.0f} pts. Gap requires structured capacity building."
            ))

        print("Seeding iGOT and NSSTA Learning Resources (DEMO_CATALOGUE)...")
        demo_resources = [
            # iGOT Karmayogi
            ("igot", "IGOT-SAM-01", "Advanced Multi-Stage Sampling for Socio-Economic Surveys",
             "Official iGOT Karmayogi course covering PPS sampling, sample size determination, variance estimation, and non-sampling error minimization.",
             "https://igotkarmayogi.gov.in/learn/advanced-sampling-techniques", "Advanced", "3 weeks",
             gov_competency_objects["STAT-02"].id),

            ("igot", "IGOT-26102-SDG", "SDG National Indicator Framework Implementation & Monitoring",
             "Practical iGOT course on MoSPI SDG guidelines, metadata templates, and inter-departmental indicator reporting protocols.",
             "https://igotkarmayogi.gov.in/learn/sdg-indicators-india", "Intermediate", "2 weeks",
             gov_competency_objects["STAT-05"].id),

            ("igot", "IGOT-26103-RSTAT", "R Programming for Government Statistical Analysis",
             "Hands-on course designed for official statisticians using R for survey weighting, tabulations, and automated statistical reporting.",
             "https://igotkarmayogi.gov.in/learn/r-official-statistics", "Beginner", "4 weeks",
             gov_competency_objects["TECH-02"].id),

            ("igot", "IGOT-26104-CYBER", "Cybersecurity and DPDP Act Compliance in Public Data Systems",
             "Training module on data privacy, confidential microdata access protection, and CERT-In security directives for official databases.",
             "https://igotkarmayogi.gov.in/learn/cybersecurity-governance", "Intermediate", "2 weeks",
             gov_competency_objects["GOV-01"].id),

            # NSSTA TPAC
            ("nssta", "NSSTA-TPAC-01", "NSSTA Training Programme on Price Index Compilation & Rebasing",
             "Residential & online hybrid training by NSSTA Greater Noida on CPI and WPI computation methodologies, price quotation validation, and index rebasing.",
             "https://mospi.gov.in/nssta/training/price-statistics-2026", "Advanced", "1 week",
             gov_competency_objects["STAT-04"].id),

            ("nssta", "NSSTA-TPAC-02", "NSSTA GIS & Spatial Statistical Analysis for District Profiling",
             "Executive workshop on spatial data visualization, QGIS integration with census boundary shapefiles, and spatial autocorrelation.",
             "https://mospi.gov.in/nssta/training/gis-spatial-analytics", "Intermediate", "5 days",
             gov_competency_objects["TECH-04"].id),

            # Industry
            ("industry", "IND-SQL-01", "Enterprise SQL: Analytics Engineering & Data Modeling",
             "Comprehensive course on window functions, CTEs, indexing, and star-schema analytical database queries.",
             "https://learning.industry.org/courses/enterprise-sql", "Intermediate", "4 weeks",
             ind_competency_objects["IND-SQL"].id),

            ("industry", "IND-BI-01", "Power BI Desktop & Service for Executive Dashboards",
             "Building interactive KPI reports, DAX time intelligence calculations, and publishing reports to Power BI Service.",
             "https://learning.industry.org/courses/powerbi-executive", "Intermediate", "3 weeks",
             ind_competency_objects["IND-BI"].id),

            # Academia
            ("academia", "ACAD-STAT-01", "Statistical Inference and Hypothesis Testing Lab",
             "University course with interactive Jupyter notebooks for hypothesis tests, ANOVA, regression analysis, and simulation.",
             "https://curriculum.univ.edu.in/labs/statistical-inference", "Academic Core", "6 weeks",
             acad_competency_objects["ACAD-STAT"].id),
        ]

        for prov_type, ext_id, title, desc, url, lvl, dur, comp_id in demo_resources:
            res = LearningResource(
                provider_type=prov_type,
                provider_external_id=ext_id,
                title=title,
                description=desc,
                url=url,
                level=lvl,
                duration=dur,
                is_demo=True,
                metadata_json={"source": "DEMO_CATALOGUE", "verified": True}
            )
            db.add(res)
            db.flush()

            db.add(ResourceCompetency(
                resource_id=res.id,
                competency_id=comp_id,
                relevance_score=0.95
            ))

            # If user is Ananya and resource matches a gap, add recommendation
            if prov_type in ["igot", "nssta"]:
                db.add(Recommendation(
                    user_id=user_ananya.id,
                    resource_id=res.id,
                    competency_id=comp_id,
                    rank=1,
                    score=92.5,
                    explanation=f"Directly addresses high priority gap in {gov_competency_objects.get('STAT-02').name if comp_id == gov_competency_objects['STAT-02'].id else 'Required Domain'}. Recommended by official capacity building framework.",
                    status="suggested"
                ))

        print("Seeding Diagnostic Assessment for Government Track...")
        diag_assessment = Assessment(
            framework_id=fw_gov.id,
            type="DIAGNOSTIC",
            title="MoSPI Official Statistics Comprehensive Baseline Diagnostic",
            status="active",
            metadata_json={"duration_minutes": 30, "total_questions": 5}
        )
        db.add(diag_assessment)
        db.flush()

        questions_data = [
            (
                gov_competency_objects["STAT-01"].id,
                "In a multi-stage stratified sampling design for a national household survey, what is the primary objective of stratifying primary sampling units (PSUs)?",
                ["To maximize variance within each stratum", "To minimize variance between strata", "To ensure homogeneous units within strata and reduce sampling variance of estimates", "To eliminate non-response errors entirely"],
                2,
                "easy",
                "Stratification groups units with similar characteristics together, decreasing within-stratum variance and yielding more precise population estimates."
            ),
            (
                gov_competency_objects["STAT-02"].id,
                "When sampling with Probability Proportional to Size (PPS), what measure of size is typically used for selecting census villages or enumeration blocks?",
                ["Total geographical land area", "Household count or estimated population from the latest Census", "Number of commercial establishments", "Distance from district headquarters"],
                1,
                "medium",
                "In official socio-economic surveys (like NSS / PLFS), village or block population/household count is standardly taken as the measure of size (MOS)."
            ),
            (
                gov_competency_objects["STAT-04"].id,
                "Which index formula is standardly utilized as the base formula for compiling the Consumer Price Index (CPI) in India?",
                ["Paasche Index formula", "Laspeyres modified formula", "Fisher's Ideal formula", "Marshall-Edgeworth formula"],
                1,
                "medium",
                "CPI is compiled using the Laspeyres base-weighted price index formula with fixed base-year consumption basket weights."
            ),
            (
                gov_competency_objects["TECH-02"].id,
                "In R statistical programming, which established CRAN package is widely recognized for handling complex survey designs and sampling weights?",
                ["ggplot2", "survey", "dplyr", "keras"],
                1,
                "easy",
                "Thomas Lumley's 'survey' package in R is the standard tool for analyzing complex survey samples with strata, clusters, and weights."
            ),
            (
                gov_competency_objects["GOV-01"].id,
                "Under India's Digital Personal Data Protection (DPDP) framework, what process must be applied to statistical microdata before public release?",
                ["Plaintext export with respondent names", "Data anonymization and statistical disclosure limitation (SDL)", "Password protecting the raw CSV file only", "No modifications are required for government surveys"],
                1,
                "medium",
                "Statistical Disclosure Limitation (SDL) and robust de-identification ensure that individual survey respondents cannot be re-identified."
            ),
        ]

        for comp_id, prompt, options, correct_idx, diff, explanation in questions_data:
            db.add(AssessmentQuestion(
                assessment_id=diag_assessment.id,
                competency_id=comp_id,
                question_type="MCQ",
                difficulty=diff,
                prompt=prompt,
                options_json=options,
                answer_json=correct_idx,
                source_ref="MoSPI Survey Standards Handbook & NSSTA Core Curriculum"
            ))

        print("Seeding Diagnostic Assessment for Industry Track...")
        diag_ind = Assessment(
            framework_id=fw_ind.id,
            type="DIAGNOSTIC",
            title="Industry Analytics & AI Core Technical Diagnostic",
            status="active",
            metadata_json={"duration_minutes": 25, "total_questions": 3}
        )
        db.add(diag_ind)
        db.flush()

        ind_questions = [
            (
                ind_competency_objects["IND-SQL"].id,
                "In SQL, which analytical clause enables calculating running totals and moving averages without collapsing individual rows?",
                ["GROUP BY ROLLUP", "OVER (ORDER BY ...)", "HAVING SUM() > 0", "CROSS JOIN"],
                1,
                "medium",
                "Window functions using the OVER clause compute aggregations across row frames while preserving individual rows."
            ),
            (
                ind_competency_objects["IND-BI"].id,
                "In Microsoft Power BI data modeling, what is the best practice schema design for high performance DAX aggregations?",
                ["Normalized 3NF Snowflake Schema", "Single Denormalized Flat Table", "Star Schema with central Fact and surrounding Dimension tables", "Document NoSQL Graph Schema"],
                2,
                "easy",
                "A Star Schema provides optimal relationship paths and VertiPaq compression for Power BI and DAX engine operations."
            ),
            (
                ind_competency_objects["IND-PY"].id,
                "In Python Pandas, what is the most vectorized and memory-efficient way to handle missing values conditionally by column group?",
                ["Iterating using for loop and df.iterrows()", "df.groupby().transform(lambda x: x.fillna(x.median()))", "Python while loop appending to list", "df.to_dict() followed by key lookup"],
                1,
                "medium",
                "Transform allows vectorized imputation by group without slow Python-level row iteration."
            )
        ]
        for comp_id, prompt, options, correct_idx, diff, explanation in ind_questions:
            db.add(AssessmentQuestion(
                assessment_id=diag_ind.id,
                competency_id=comp_id,
                question_type="MCQ",
                difficulty=diff,
                prompt=prompt,
                options_json=options,
                answer_json=correct_idx,
                source_ref="Industry Analytics Standards & PEP 8 Best Practices"
            ))

        print("Seeding Diagnostic Assessment for Academia Track...")
        diag_acad = Assessment(
            framework_id=fw_acad.id,
            type="DIAGNOSTIC",
            title="Higher Education Foundational Computing & Statistical Diagnostic",
            status="active",
            metadata_json={"duration_minutes": 25, "total_questions": 3}
        )
        db.add(diag_acad)
        db.flush()

        acad_questions = [
            (
                acad_competency_objects["ACAD-STAT"].id,
                "In statistical hypothesis testing, what does a p-value strictly measure?",
                ["The probability that the alternative hypothesis is true", "The probability of observing data at least as extreme as observed, assuming the null hypothesis is true", "The probability that the null hypothesis is true", "The probability of committing a Type II error"],
                1,
                "medium",
                "The p-value is the probability under the null hypothesis of obtaining a test statistic as extreme or more extreme than observed."
            ),
            (
                acad_competency_objects["ACAD-MATH"].id,
                "In linear algebra for machine learning, if matrix A has full column rank, which condition holds true?",
                ["All eigenvalues are zero", "The column vectors are linearly independent", "The determinant is undefined", "Matrix A must be a diagonal identity matrix"],
                1,
                "easy",
                "Full column rank indicates that all column vectors are linearly independent, ensuring unique least-squares solutions."
            ),
            (
                acad_competency_objects["ACAD-DB"].id,
                "Which normal form specifically addresses transitive functional dependencies between non-prime attributes?",
                ["First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF) only"],
                2,
                "medium",
                "3NF requires that the relation is in 2NF and no non-prime attribute is transitively dependent on any candidate key."
            )
        ]
        for comp_id, prompt, options, correct_idx, diff, explanation in acad_questions:
            db.add(AssessmentQuestion(
                assessment_id=diag_acad.id,
                competency_id=comp_id,
                question_type="MCQ",
                difficulty=diff,
                prompt=prompt,
                options_json=options,
                answer_json=correct_idx,
                source_ref="University OBE Curriculum Syllabus & Discrete Mathematics"
            ))

        # Seed initial CompetencyHistory records for Ananya's baseline
        for code, score, level, conf, src in ananya_competencies:
            comp = gov_competency_objects[code]
            db.add(CompetencyHistory(
                user_id=user_ananya.id,
                competency_id=comp.id,
                assessment_attempt_id=diag_assessment.id,
                score_before=0.0,
                score_after=score,
                delta=score,
                confidence_before=0.5,
                confidence_after=conf,
                source="diagnostic"
            ))

        print("Seeding Audit Event...")
        db.add(AuditEvent(
            actor_id=user_admin.id,
            organization_id=org_mospi.id,
            action="SYSTEM_INIT_SEED",
            entity_type="SYSTEM",
            entity_id=fw_gov.id,
            metadata_json={"details": "Deterministic seed completed successfully for STAT-SKILL AI production baseline."}
        ))

        db.commit()
        print("Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
