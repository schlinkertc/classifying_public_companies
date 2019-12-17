# Classifying Public Companies
Given certain balance sheet and cash flow metrics, can we reasonably predict whether or not a company is in the manufacturing industry?

### Overview
Data was gathered directly for financial statements submitted to the SEC. The model considered assets; liabilites & stockholder's equity; net income; and cash flows from operating, financing, and investing activitie. The model uses a random forest classifier to make its predictions. In it's current state, the model is inconclusive. The model will be imporved with additional features and modeling techniques. 

## Data Gathering

Financial statements provided by the SEC are organized into 4 tables representing submissions, numbers, tags, and presentations. The submissions table provides a unique record for every submission the SEC has received that quarter. The numbers table provides each numerical value that corresponds to a unique submission. The number is described in the tag table, and the presentation table shows were the number appeared in the corresponding financial statement. 

Numbers are tagged using XBRL,or eXtensible Business Reporting Language. The primaryf challenge of this classification model was identifying XRBL tags that are used commonly across a suffecient number of companies to make legitmate comparisons. I discovered that companies use XBRL tags slightly differently, and even the tags that were used for a majority of public companies can mean vastly different things depending on the context. Ultimately, I'm not confident that the data gathered can be reliably used for statistical modeling. 

In order to make legitmate conclusions from this data, ...

## 



