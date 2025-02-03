from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load dataset
df = pd.read_csv("netflix_titles.csv")


# Function to generate Plotly charts
def generate_charts():
    # Count Movies vs TV Shows and rename columns
    content_counts = df['type'].value_counts().reset_index()
    content_counts.columns = ['Content Type', 'Count']

    # Bar chart: Movies vs TV Shows
    bar_chart = px.bar(content_counts,
                       x='Content Type', y='Count',
                       labels={'Content Type': 'Content Type', 'Count': 'Count'},
                       title="Netflix Movies vs TV Shows", color='Content Type')

    # Pie chart: Distribution of Content Ratings
    pie_chart = px.pie(df, names='rating', title="Distribution of Ratings")

    # Line Chart: Yearly Content Additions
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    yearly_data = df.groupby('release_year').size().reset_index(name='count')
    line_chart = px.line(yearly_data, x='release_year', y='count', title="Netflix Content Over the Years")

    return bar_chart.to_html(full_html=False), pie_chart.to_html(full_html=False), line_chart.to_html(full_html=False)


@app.route('/')
def index():
    bar_chart, pie_chart, line_chart = generate_charts()
    return render_template("index.html", bar_chart=bar_chart, pie_chart=pie_chart, line_chart=line_chart)


@app.route('/data')
def data():
    return render_template("data.html", table_data=df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
