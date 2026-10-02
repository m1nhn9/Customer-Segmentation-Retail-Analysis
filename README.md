<div align="center">
  <img width="320px" src="https://via.placeholder.com/320x80?text=Customer+Segmentation" />
</div>
<h1 align="center">E-Commerce Customer Segmentation Analysis</h1>
<table align="center">
  <tr>
    <td width="1440">
      <h2 align="center">Project Background</h2>
      <body>
        This project analyzes customer behavior for a <strong>UK-based online retailer</strong> using transactional data spanning 500,000+ rows. The goal was to move the marketing team away from a "mass-marketing" approach toward highly targeted, data-driven strategies. <br>
        <br>
        Using the <strong>RFM (Recency, Frequency, Monetary)</strong> framework combined with <strong>K-Means Clustering</strong>, customers were grouped into distinct segments to inform personalized marketing campaigns and retention strategies. <br>
        <br>
        The analysis was conducted using <strong>SQL (PostgreSQL)</strong> for data engineering and <strong>Python (Pandas, Scikit-Learn, Seaborn)</strong> for machine learning and visualization. The key insights and recommendations focus on the following areas:
      </body>
      <h3>Northstar Metrics</h3>
      <h4>
        <ul>
          <li>Customer segmentation - Grouping customers into actionable clusters using RFM scoring and K-Means Clustering.</li>
          <li>Recency analysis - Identifying customers at risk of churn based on time since last purchase.</li>
          <li>Frequency & monetary behavior - Understanding purchase patterns and spend levels across segments.</li>
          <li>Marketing recommendations - Providing targeted strategies for each customer segment to maximize retention and revenue.</li>
        </ul>
      </h4>
    </td>
  </tr>
</table>

<table align="center">
  <tr>
    <div width="920">
      <h1 align="center">Executive Summary</h1>
      <td width="460" valign="top">
        <ol>
          <li>
            <strong>Champions & Loyalists Drive Revenue:</strong>
            <ul>
              <li>Champions are the highest-value segment — high spenders, frequent buyers, and most recently active customers.</li>
              <li>Loyalists show consistent purchasing behavior with strong spend, making them prime candidates for upselling and VIP programs.</li>
            </ul>
          </li>
          <li>
            <strong>New/Recent Customers Show Growth Potential</strong>
            <ul>
              <li>This segment has high recency but low frequency, indicating they are early in their customer lifecycle.</li>
              <li>A targeted second-purchase incentive could convert them into long-term Loyalists.</li>
            </ul>
          </li>
        </ol>
      </td>
      <td width="460" valign="top">
        <ol start="3">
          <li>
            <strong>At-Risk Customers Require Immediate Action</strong>
            <ul>
              <li>At-Risk customers haven't purchased in 6+ months, signaling a high probability of churn.</li>
              <li>Re-engagement campaigns with personalized "We Miss You" offers could recover a meaningful share of this segment.</li>
            </ul>
          </li>
          <li>
            <strong>Key Takeaways & Recommendations</strong>
            <ul>
              <li>Shift from mass-marketing to segment-specific campaigns to maximize ROI.</li>
              <li>Prioritize Champions and Loyalists for VIP and retention programs.</li>
              <li>Deploy win-back campaigns for At-Risk customers before they churn permanently.</li>
            </ul>
          </li>
        </ol>
      </td>
    </div>
  </tr>
</table>

<h2 align="center">Dataset Structure</h2>
<body>The dataset consists of raw transactional logs from a UK-based online retailer with over <strong>500,000 rows</strong>. After cleaning (removing missing Customer IDs and filtering cancellations), data was aggregated into RFM metrics per customer.</body>

<h2 align="center">Cluster Sizes & Share of Revenue</h2>

Re-running the same cleaning rules and K-Means model (k=4, `random_state=42`) on the raw [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) file with `rebuild_rfm.py`: 541,909 raw rows → 392,689 clean rows → **4,338 customers**, £8.89M total spend. Amounts are in pounds sterling (£).

| Segment | Customers | % of customers | Avg days since last order | Avg orders | Avg spend | % of revenue |
|---|---:|---:|---:|---:|---:|---:|
| Champions | 718 | 16.6% | 12 | 13.6 | £8,011 | **64.7%** |
| Loyalists | 1,174 | 27.1% | 65 | 4.2 | £1,823 | 24.1% |
| New / Recent | 897 | 20.7% | 23 | 1.9 | £486 | 4.9% |
| At-Risk | 1,549 | 35.7% | 192 | 1.4 | £361 | 6.3% |

Champions and Loyalists are 44% of customers but 89% of revenue. K-Means cluster numbers are arbitrary, so segment names are assigned from each cluster's averages. To reproduce: `python3 rebuild_rfm.py "Online Retail.xlsx"` (needs `pandas`, `openpyxl`, `scikit-learn`). `missing_step.sql` adds the `cleaned_retail_data` table that the RFM queries in `sql_scripts.sql` read from.

<h2 align="center">Power BI Dashboard</h2>

![Customer Segmentation Power BI dashboard](powerbi/dashboard.png)

The [`powerbi/`](powerbi) folder has a Power BI project built on the same segments. It holds a one-page dashboard (KPIs, segment/country/month filters, monthly revenue by segment, customer vs revenue share, top countries, a customer list and the segment action plan), detail pages and an Insights page. `rebuild_rfm.py` writes the two CSVs it loads; see [`powerbi/README.md`](powerbi/README.md) for how to open it.

<h1 align="center">Insights Deep-Dive</h1>

<table align="center">
  <tr>
    <h1 align="center">RFM Segmentation</h1>
    <td width="1000">
      <h3 align="center">Elbow Method</h3>
      <img width="300" src="https://github.com/m1nhn9/Customer-Segmentation-Retail-Analysis/blob/main/visuals:/elbow_plot.png?raw=true">
    </td>
    <td width="1000">
      <h3 align="center">Snake Plot</h3>
      <img width="300" src="https://github.com/m1nhn9/Customer-Segmentation-Retail-Analysis/blob/main/visuals:/snake_plot.png?raw=true">
    </td>
    <td width="1000">
      <h3 align="center">Attribute Heatmap</h3>
      <img width="300" src="https://github.com/m1nhn9/Customer-Segmentation-Retail-Analysis/blob/main/visuals:/cluster_heatmap.png?raw=true">
    </td>
  </tr>
</table>

<table>
  <tr>
    <td>
      <strong>Optimal Cluster Selection (Elbow Method)</strong>
      <ol>
        <li>Mathematically Determined k=4 as Optimal
          <ul>
            <li>The elbow plot showed diminishing returns in inertia reduction beyond 4 clusters, confirming k=4 as the ideal number of segments.</li>
            <li>This prevents over-segmentation while ensuring each cluster is meaningfully distinct.</li>
          </ul>
        </li>
      </ol>
      <strong>Customer Segment Behavior (Snake Plot)</strong>
      <ol>
        <li>Clear Differentiation Across RFM Dimensions
          <ul>
            <li>Champions score highest across all three RFM metrics — most recent, most frequent, and highest spend.</li>
            <li>At-Risk customers show the inverse pattern — low recency, low frequency, and low monetary value — making them the most vulnerable to permanent churn.</li>
          </ul>
        </li>
        <li>New/Recent Customers Show Recency Without Depth
          <ul>
            <li>High recency scores but low frequency and monetary values indicate first-time or infrequent buyers with untapped potential.</li>
          </ul>
        </li>
      </ol>
      <strong>Attribute Importance Heatmap</strong>
      <ol>
        <li>Recency is the Primary Churn Indicator
          <ul>
            <li>Recency is the strongest differentiator between Champions and At-Risk customers.</li>
            <li>Monetary value is the key defining trait of Champions and Loyalists, separating high-value from low-value segments.</li>
          </ul>
        </li>
      </ol>
    </td>
  </tr>
</table>

<table align="center">
    <h1 align="center">Recommendations</h1>
    <h4>Based on the uncovered insights, here are actionable items the marketing team can apply per customer segment.</h4>
      <h3>Champions</h3>
      <ul>
        <li>Invite to an exclusive <strong>VIP Loyalty Program</strong> with early access to new products and members-only discounts.</li>
          <ul><li>This segment drives the highest revenue and has the strongest engagement — retaining them has outsized business impact.</li></ul>
      </ul>
      <h3>Loyalists</h3>
      <ul>
        <li>Offer <strong>tiered rewards</strong> and personalized product recommendations to increase purchase frequency.</li>
          <ul><li>Loyalists are one step away from Champion status — targeted nudges can elevate their lifetime value significantly.</li></ul>
      </ul>
      <h3>New / Recent Customers</h3>
      <ul>
        <li>Send a <strong>"second-purchase" discount code</strong> within 7 days of their first order to build purchase habit.</li>
          <ul><li>Converting new customers into repeat buyers is the most cost-effective path to growing the Loyalist segment.</li></ul>
      </ul>
      <h3>At-Risk Customers</h3>
      <ul>
        <li>Launch a <strong>re-engagement email campaign</strong> with a personalized "We Miss You" offer and time-limited incentive.</li>
          <ul><li>Customers inactive for 6+ months are at critical risk of permanent churn — a win-back offer can recover a meaningful share before they disengage entirely.</li></ul>
      </ul>
</table>

---
**Author:** Minh Nguyen  
**Contact:** https://www.linkedin.com/in/minhng224/
