# Finance Tracker and Visualizer 
A tool for keeping track of budget as well as daily and weekly accumulated expenditures across different categories of expenses. Provides data visualization with bar graph and pie chart options.

## Technologies Used
- **Frontend**: React, HTML, CSS, Typescript, Chart.js
- **Backend**: Python, Flask, SQLite3

## Features & Functionality  
- **Components**: Utilizes React components to build reusable UI elements. Certain pages and features are encapsulated in their own component, improving maintainability and readability of the code.  
- **Dynamically Rendered Components**: Pie and and bar charts are rendered conditionally based on user preference.  
- **Passing Props**: Components communicate and share data through props, allowing for dynamic content rendering and a smooth user experience. For example, the main page component passes data to child components to display relevant content.  
- **Live-updating Data Visualization**: Weekly and daily accumulated expenditures are visualized in real-time using Chart.js Bar and Pie chart components.
- **Accumulated Expenditure Tracking**: Server handles logic for accumulating expenditures across expenditure categories and across days and weeks.  
- **Automatic Recurring Expenditures**: Server automatically adds weekly recurring expenditures.
