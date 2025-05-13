import React from "react";
import { Bar } from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { ChartData, ChartOptions } from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

interface ExpenseEntry {
  ID: number;
  Date: string;
  Housing: number;
  Transportation: number;
  Food: number;
  Clothes: number;
  Healthcare: number;
  PersonalCare: number;
  Education: number;
  DebtPayments: number;
  SavingsInvestments: number;
  Entertainment: number;
  GiftsDonations: number;
  Misc: number;
  Total: number;
}

const ExpenseBarChart = ({ myProp }: { myProp: ExpenseEntry[] }) => {
  if (!myProp || myProp.length === 0) {
    return <p>No data to display</p>;
  } else {
    console.log("react state logged: ");
    console.log(myProp);

    // const testdata: ExpenseEntry[] = [
    //   {
    //     id: 1,
    //     date: "2025-05-01",
    //     housing: 100,
    //     transportation: 5,
    //     food: 20,
    //     clothes: 0,
    //     healthcare: 0,
    //     personalCare: 0,
    //     education: 0,
    //     debtPayments: 0,
    //     savingsInvestments: 0,
    //     entertainment: 0,
    //     giftsDonations: 0,
    //     misc: 0,
    //     total: 0,
    //   },
    // ];

    const dataObject = myProp[0];

    console.log(dataObject);

    const labels = Object.keys(dataObject).filter(
      (key) => !["ID", "Date"].includes(key),
    ) as (keyof ExpenseEntry)[];

    const values = labels.map((label) => dataObject[label] as number);

    const data: ChartData<"bar"> = {
      labels,
      datasets: [
        {
          label: "Expenses ($)",
          data: values,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderRadius: 5,
        },
      ],
    };

    const options: ChartOptions<"bar"> = {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: `Expenses on ${dataObject.Date}`,
        },
      },
    };

    return (
      <div style={{ maxWidth: "700px", margin: "0 auto" }}>
        <Bar data={data} options={options} />
      </div>
    );
  }
};

export default ExpenseBarChart;
