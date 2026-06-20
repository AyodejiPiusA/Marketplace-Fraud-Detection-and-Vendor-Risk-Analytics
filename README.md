# # Marketplace Fraud Detection and Vendor Risk Analytics
## Inspiration
In May 2026, Techpoint Africa published an investigation into weaknesses in vendor onboarding processes on food-delivery platforms. The investigation demonstrated how a fake restaurant could be successfully onboarded onto delivery platforms using fabricated business information, stolen restaurant images, and minimal verification checks. The article raised important questions around:
* Vendor impersonation
* Business verification controls
* Image authenticity checks
* Fraud prevention in marketplace ecosystems
* Trust & Safety operations
This project was inspired by that investigation and explores how data analytics could be used to identify suspicious vendors, prioritize investigations, and reduce marketplace risk.

Source: https://techpoint.africa/insight/investigation-glovo-and-chowdeck-onboarding-process/

## Project Overview
Inspired by public reporting on vendor impersonation and verification weaknesses in food-delivery marketplaces, this project simulates a Trust & Safety investigation into fraudulent vendor activity, onboarding vulnerabilities, and refund related financial losses. Using Python, SQL, and Power BI, I designed a synthetic food delivery marketplace consisting of vendors, customer orders and image verification records. The objective was to demonstrate how data analytics can be used to identify suspicious vendors, uncover fraud patterns, prioritize investigations, and strengthen marketplace integrity. The final output is an interactive Power BI dashboard that enables Trust and Safety, Operations, and Risk teams to monitor fraud indicators and take proactive action before losses escalate.

---

## Business Problem
Food delivery platforms rely on trust between customers, vendors, and platform operators. Weak verification processes can create opportunities for bad actors to:
* Create synthetic vendor accounts
* Operate without valid business registration
* Reuse stolen or scraped marketing images
* Generate excessive refunds and customer complaints
* Exploit onboarding gaps before detection
This project explores how operational and compliance data can be leveraged to identify these risks early and support more effective vendor monitoring.

---

## Project Objectives
The project was designed to answer the following questions:
* Which vendors present the highest operational risk?
* Are refund losses concentrated among specific vendor groups?
* Can image provenance serve as a useful fraud signal?
* How effective are current verification controls?
* How can Trust & Safety teams prioritize investigations?

---

## Dataset Design
To simulate marketplace operations, three linked datasets were generated using Python. The data model utilizes a central Dimension Table (Vendors) linked to two Fact/Detail Tables (Orders and Images) via a One-to-Many relationship architecture.
* Vendors (1) ➔ (Many) Orders: Connected via Vendor_ID. (A single vendor can process thousands of orders).
* Vendors (1) ➔ (Many) Images: Connected via Vendor_ID. (A single vendor can upload multiple profile and menu images).

### Dataset Design
To simulate marketplace operations, three linked datasets were generated using Python. The synthetic data was intentionally designed to model both legitimate and suspicious behavior, including unverified business registrations, elevated refund frequencies, and duplicate image usage.

#### 1. Vendors Dataset (Dimension Table)
**Description:** The primary entity table storing all demographic, operational, compliance, and algorithmic risk metrics for the 260 marketplace restaurants.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`vendor_id`** | `Text` | *(Primary Key)* Unique alphanumeric identifier for each vendor entity. |
| **`restaurant_name`** | `Text` | The registered business name on the marketplace. |
| **`signup_date`** | `Date` | The date the vendor registered on the platform. |
| **`city`** | `Text` | The operational city of the vendor. |
| **`address`** | `Text` | The physical registered address of the vendor. |
| **`phone_number`** | `Text` | Contact number provided during onboarding. |
| **`bank_account`** | `Text` | Settlement account details where payouts are sent. |
| **`cac_verified`** | `Boolean/Text` | Indicates if the Corporate Affairs Commission registration is legally validated. |
| **`tin_verified`** | `Boolean/Text` | Indicates if the Tax Identification Number is actively matched to the entity. |
| **`account_type`** | `Text` | The vendor's financial settlement destination. |
| **`duplicate_image_score`** | `Decimal` | An algorithmic score indicating the vendor's usage of scraped or duplicated visual imagery. |
| **`refund_rate`** | `Percentage` | The historical percentage of total orders that resulted in a customer refund. |
| **`delivery_failure_rate`** | `Percentage` | The percentage of dispatched orders that failed to reach the customer. |
| **`risk_score`** | `Whole Number` | A calculated algorithmic score based on operational and compliance risk indicators. |
| **`risk_category`** | `Text` | The operational risk tier assigned based on the Risk Score. |
| **`fraud_label`** | `Text` | Ground truth operational classification used for filtering. |

#### 2. Orders Dataset (Fact Table)
**Description:** The transactional log recording all 5,000 individual food delivery requests, financial amounts, and customer outcomes.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`order_id`** | `Text` | *(Primary Key)* Unique alphanumeric identifier for the transaction. |
| **`vendor_id`** | `Text` | *(Foreign Key)* Links the transaction to the specific vendor. |
| **`order_amount`** | `Decimal` | The total gross monetary value of the transaction in NGN (₦). |
| **`order_timestamp`** | `Date/Time` | The exact date and time the transaction was initiated. |
| **`delivery_status`** | `Text` | The terminal state of the order. |
| **`customer_rating`** | `Whole Number` | The feedback score (1-5 stars) provided by the customer. |
| **`refund_requested`** | `Boolean` | True/False flag indicating if the customer initiated a refund claim. |

#### 3. Images Dataset (Metadata Table)
**Description:** A detailed log of the 780 image assets uploaded by vendors, utilized to track visual provenance and detect scraped assets.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`image_id`** | `Text` | *(Primary Key)* Unique identifier for the uploaded image file. |
| **`vendor_id`** | `Text` | *(Foreign Key)* Links the image asset to the uploading vendor profile. |
| **`duplicate_score`** | `Decimal` | A confidence score indicating if the specific image matches an existing asset. |
| **`image_source_class`** | `Text` | The origin of the image detected by the system (e.g., Original Upload, Social Media). |

---

### Risk Scoring Framework
A rule-based risk scoring model was developed to classify the vendors from the dataset above based on operational and compliance signals. This framework enables Trust & Safety teams to prioritize investigations and allocate resources more effectively.

#### Risk Indicators
| Risk Indicator | Points |
| :--- | :--- |
| Invalid TIN | 25 |
| High Duplicate Image Score | 20 |
| Personal Settlement Account | 15 |
| Elevated Refund Rate | 20 |
| High Delivery Failure Rate | 10 |

#### Risk Categories
Based on the cumulative score, vendors are segmented into:
* **Low Risk**
* **Medium Risk**
* **Critical Risk**

---
The synthetic data was intentionally designed to model both legitimate and suspicious behavior, including:

* Fraud rings sharing contact details and payout information
* Unverified business registrations
* Elevated refund frequencies
* High delivery failure rates
* Duplicate image usage

---

## Tools Used

### Python
Used to generate realistic synthetic marketplace data and simulate fraud patterns.

### SQL
Used for exploratory analysis, aggregation, fraud investigation, and risk assessment.
Examples of analysis performed:
* Refund concentration analysis
* Vendor risk segmentation
* Compliance gap identification
* High-risk vendor ranking
* Fraud ring investigation

### Power BI
Used to:
* Model relationships between datasets
* Create DAX measures
* Design interactive dashboards
* Build fraud monitoring visuals

---
## Key Findings

### 1. Scraped Images Are a Strong Predictor of Transactional Failure 
Analysis showed that vendor image authenticity is a significant risk indicator. Vendors utilizing scraped social media images exhibited a refund rate rate of 42.3%, compared to 25.3% for vendors using original uploads. This suggests that implementing automated image screening at onboarding could proactively flag highly risky subset of vendors for further review before they become operational.

---
### 2. Verification Gaps Create Elevated Risk
Vendors operating without successful CAC and TIN verification consistently exhibited higher risk scores, increased refund activity, and poorer operational performance. This is highlighted by critical risk vendors driving a 71.4% refund rate, compared to 37% for medium risk and a baseline of 25.5% for low risk vendors. This emphasizes the importance of strengthening onboarding controls before vendors become operational.

---

### 3. Image Provenance Is a Valuable Fraud Signal
Vendor image authenticity is not just a risk factor, it is a primary identifier for severe platform abuse. the data showed that 100% of the critical risk vendors relied entirely on scraped social media images, generating a massive 71.4% refund rate across their 35 total orders. This demonstrates how image verification and reverse-image screening could provide an additional layer of fraud prevention during onboarding.

---

### 4. Fraud Networks Leave Detectable Patterns and Concentrate Platform Damage
The synthetic data reveals that when bad actors operates in coordinated networks (fraud ring), the negative impact is exceptionally high, resulting in a severe 78.6% refund rate. However, these synthetic fraud rings leave detectable patterns by often sharing common identifiers such as:
* Bank accounts
* Phone numbers
* Addresses
Because this vendors also exclusively uses scraped social media images, combining image proverance checks with with network based identifiers tracking will severely undermine coordinated fraud efforts.

---

### 5. High Transaction Volumes Drive The Largest Capital Drain
While low risk vendors maintain the healthiest refund rate on the platform at 25.5%, their massive transcation volume of 4938 orders results in the platform's highest total total finacial outflow, accounting for approximately 17 Million Naira in cummulative refunds. This highlights the need to optimize standard vendor fulfilment and customer satisfaction.

---

## Recommendations

### Mandate Strict Onboarding Verification

Require successful CAC and TIN validation before vendors are permitted to operate on the platform. This directly addresses Finding 2, which proves that verification gaps allow critical risk vendors to bypass controls and drive a massive 71.4% refund rate.

---

### Implement Automated Image Verification Checks

Deploy automated  reverse-image screening solutions to identify duplicated or externally sourced content during the vendor application process. Findings 1 and 3 demonstrate that scraped social media images are a primary fraud signal, with 100% of critical risk vendors relying entirely on social media sourced images. Proactive denial based on image source will immediately neutralize this vunerabilty.

---

### Introduce Network-Based Monitoring

Implement link-analysis controls that flag vendors sharing common identifiers, specifically:
* Bank accounts
* Phone numbers
* Registered addresses
* Device fingerprints
Finding 4 reveals that synthetic fraud rings cause severe platform damage with 78.6% refund rate but leave detectable patterns. Tracking these connections will improve the detection of coordinated fraud activity.

---

### Optimize Standard Vendor Fulfilment

Establish operational improvement programs focused on reducing normal operational refund drivers such as inventory management or fulfillment speed across the broader marketplace. This directly addresses Finding 5. While fraud prevention targets severe abuse, standardizing operations is required to curb low risk vendors refund rate. 

---

### Transition to Dynamic Risk Based Monitoring

A shift from relying solely on static initial verification to continuous behavioral monitoring. Operations teams should prioritize investigations using dynamic risk scores focused on:
* Rapid activity or volume spikes
* Escalating refund frequency
Continuous monitoring ensures that high risk accounts that manage to bypass initial onboarding checks can be frozen before their potential losses scale.

---

## Dashboard 

### Overview
<img width="590" height="329" alt="Screenshot 2026-06-08 135544" src="https://github.com/user-attachments/assets/fe09f1b6-92bd-41dc-add1-5202c032b302" />

### Filtered Investigation View

<img width="586" height="332" alt="Screenshot 2026-06-11 212528" src="https://github.com/user-attachments/assets/08797bb0-a62f-4f3f-8be7-09fe36e60a36" />

<img width="590" height="332" alt="Screenshot 2026-06-11 212639" src="https://github.com/user-attachments/assets/61fb24be-5869-439d-90e0-44fa762d8566" />

---

## Limitations

This project uses synthetic data generated for educational and portfolio purposes.

The fraud patterns, operational behaviors, and risk signals were intentionally designed to simulate realistic marketplace scenarios and demonstrate analytical techniques. The findings should be interpreted as illustrative examples rather than evidence of actual platform activity.

---

## Author

Built by Ayodeji Pius using Python, SQL, and Power BI to explore Trust and Safety analytics, marketplace risk detection, and operational fraud investigation.
