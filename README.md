# Finance Tracker and Visualizer 
A tool for keeping track of budget as well as daily and weekly accumulated expenditures across different categories of expenses. Provides data visualization with bar graph and pie chart options.

## Video Demonstration

The following video demonstrates input multiple transactions over days and weeks across multiple categories. Budget tracking is featured as well. The viewer is encouraged to skip to sections relevant to their interests for convenience.

https://drive.google.com/drive/folders/1BjPJg5_kcNysFIH6wSktdlNe19m3vRns

## Technologies Used
- **Frontend**: React, HTML, CSS, TypeScript, Chart.js
- **Backend**: Python, Flask, SQLite3

## Features & Functionality  
- **Components**: Utilizes React components to build reusable UI elements. Certain pages and features are encapsulated in their own component, improving maintainability and readability of the code.  
- **Dynamically Rendered Components**: Pie and and bar charts are rendered conditionally based on user preference.  
- **Passing Props**: Components communicate and share data through props, allowing for dynamic content rendering and a smooth user experience. For example, the main page component passes data to child components to display relevant content.  
- **Live-updating Data Visualization**: Weekly and daily accumulated expenditures are visualized in real-time using Chart.js Bar and Pie chart components.
- **Accumulated Expenditure Tracking**: Server handles logic for accumulating expenditures across expenditure categories and across days and weeks.  
- **Automatic Recurring Expenditures**: Server automatically adds weekly recurring expenditures. Recurring expenditures are added to both weekly and daily expenditures (Added to the first day of the week for daily expenditures).  
- **Out-pacing Budget Warning**: Server notifies client if user is on track to exceed weekly budget.
- **Expense Table to PDF Conversion**: Converts weekly expenses table to PDF file for user records.

## Challenges & Solutions

- **Challenge**: Desired for server to send "out pacing weekly budget" message to client on the event of daily total exceeding a set limit but not on successive additions over the limit.
- **Solution**: Set "out pacing weekly budget" boolean to false on every entry to daily expense table. Another boolean variable only allows "out pacing weekly budget" boolean to be set to true once in a day.
