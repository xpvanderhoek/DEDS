import sqlite3

from sklearn import metrics
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree


go_sales = sqlite3.connect('../week1/Data/go_sales_train.sqlite')

order_details = pd.read_sql(
    """
    SELECT 
        order_details.ORDER_DETAIL_CODE,
        order_details.ORDER_NUMBER,
        order_details.PRODUCT_NUMBER,
        order_details.QUANTITY,
        order_details.UNIT_COST,
        order_details.UNIT_PRICE,
        order_details.UNIT_SALE_PRICE,
        returned_item.RETURN_REASON_CODE
    FROM 
        order_details
    LEFT JOIN 
        returned_item 
    ON 
        returned_item.ORDER_DETAIL_CODE = order_details.ORDER_DETAIL_CODE
    WHERE returned_item.RETURN_REASON_CODE IS NOT NULL
    """,
    go_sales
)

features = ['QUANTITY', 'UNIT_COST', 'UNIT_PRICE', 'UNIT_SALE_PRICE']
target = 'RETURN_REASON_CODE'

model_df = order_details[features + [target]]

X = model_df[features]
y = model_df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

dtree = DecisionTreeClassifier(max_depth = 2)
dtree = dtree.fit(X_train, y_train)
tree.plot_tree(dtree, feature_names = X.columns)
plt.show()

predicted_df = pd.DataFrame(dtree.predict(X_test))
predicted_df = predicted_df.rename(columns = {0 : 'Predicted_Return'})
model_results_frame = pd.concat([y_test.reset_index()['RETURN_REASON_CODE'], predicted_df], axis = 1)

# Zorg dat je alle unieke labels ophaalt
unique_labels = sorted(y.unique())

# Teken de confusion matrix met juiste labels
cm_display = ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=unique_labels, xticks_rotation=45)

plt.title("Confusion Matrix - Retourreden voorspellen")
plt.tight_layout()
plt.show()
print("Accuracy:", accuracy_score(y_test, y_pred), "\n")

plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=1)

plt.title("Werkelijke vs Voorspelde Waarden (Retourredenen)")
plt.xlabel("Werkelijke Waarde")
plt.ylabel("Voorspelde Waarde")
plt.grid(True)
plt.tight_layout()
plt.show()