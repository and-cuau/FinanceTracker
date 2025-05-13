import { useEffect, useRef, useState } from "react";
import "../App.css";
import { Link } from "react-router-dom";
import Chart from "chart.js/auto"; // Import Chart.js

import ExpenseBarChart from "./BarChart";
import ExpensePieChart from "./PieChart";
import MeterChart from "./MeterChart";

export default function Home() {
  //   const [expenditures, setExpenditures] = useState<any[]>([]);
  const [isPie, setIsPie] = useState(false);

  const [selected, setSelected] = useState("Housing");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");

  const [inputBudget, setInputBudget] = useState<string>("");
  const [budget, setBudget] = useState<string>("30");
  // const [tbudget, tsetBudget] = useState<number | undefined>();

  //   const tableBodyRef = useRef<HTMLTableSectionElement | null>(null);

  const [transactions, setTransactions] = useState<any[]>([]);
  const [expenditures, setExpenditures] = useState<any[]>([]);
  const [weeklyExpenditures, setWeeklyExpenditures] = useState<any[]>([]);

  function fetchTransactions() {
    fetch("http://127.0.0.1:8000/transactions", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Transactions received:", data);
        setTransactions(data);
      })
      .catch((error) => console.error("Error fetching transactions:", error));
  }

  function fetchExpenditures() {
    fetch("http://127.0.0.1:8000/expenditures", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Expenditures received:", data);

        setExpenditures(data);
      })
      .catch((error) => console.error("Error fetching expenditures:", error));
  }

  function fetchWeeklyExpenditures() {
    fetch("http://127.0.0.1:8000/weekly_expenditures", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Weekly Expenditures received:", data);

        setWeeklyExpenditures(data);
      })
      .catch((error) =>
        console.error("Error fetching weekly expenditures:", error),
      );
  }

  async function sendFetchData() {
    console.log("testsendfetch");

    const dataObj = { option: selected, amount: amount, date: date };

    try {
      const weeklyRes = await fetch(
        "http://127.0.0.1:8000/weekly_expenditures",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dataObj),
        },
      );
      const weeklyData = await weeklyRes.json();

      const expRes = await fetch("http://127.0.0.1:8000/expenditures", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dataObj),
      });
      const expData = await expRes.json();

      const transRes = await fetch("http://127.0.0.1:8000/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dataObj),
      });
      const transData = await transRes.json();

      fetchWeeklyExpenditures();
      fetchExpenditures();
      fetchTransactions();
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function shortenYear(dateStr: String) {
    const parts = dateStr.split("/");
    if (parts.length !== 3) {
      throw new Error("Invalid date format. Expected MM/DD/YYYY");
    }
    const [month, day, year] = parts;
    return `${month}/${day}/${year.slice(-2)}`;
  }

  useEffect(() => {
    console.log("Component mounted");

    fetchWeeklyExpenditures();
    fetchExpenditures();
    fetchTransactions();

    // Optional cleanup function
    return () => {
      console.log("Component unmounted");
    };
  }, []); // Empty dependency array

  return (
    <>
      <h1>MyFinanceSite</h1>
      <label htmlFor="options">Choose an option:</label>

      <div>
        <select
          id="options"
          name="options"
          onChange={(e) => {
            const action = e.target.value;
            setSelected(action);
          }}
        >
          <option value="Housing">Housing</option>
          <option value="Transportation">Transportation</option>
          <option value="Food">Food</option>
          <option value="Clothes">Clothes</option>
          <option value="Healthcare">Healthcare</option>
          <option value="PersonalCare">Personal Care</option>
          <option value="Education">Education</option>
          <option value="DebtPayments">Debt Payments</option>
          <option value="SavingsInvestments">Savings & Investments</option>
          <option value="Entertainment">Entertainment</option>
          <option value="GiftsDonations">Gifts & Donations</option>
          <option value="Misc">Misc.</option>
        </select>

        <label htmlFor="amount">$</label>
        <input
          type="text"
          id="userInput"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="Amount"
        />

        <input
          type="text"
          id="dateInput"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          placeholder="Date"
        />

        <button onClick={() => sendFetchData()}>Send</button>
        <h2 className= "weeklybudget">Weekly Budget</h2>
      </div>

    

      <div>
        <input
          type="text"
          id="budgetInput"
          value={inputBudget}
          onChange={(e) => setInputBudget(e.target.value)}
          placeholder="Budget"
        />
        <button onClick={() => setBudget(inputBudget)}></button>
      </div>

      <button onClick={() => setIsPie(!isPie)}>
        {isPie ? "Bar Graph" : ""}
      </button>

      <div className="dash">
        <div className="charts">
          <div style={{ padding: "2em" }}>
            <h2>Weekly Budget Meter</h2>
            <MeterChart value={10} budget={parseInt(budget)} />
          </div>

          {isPie ? (
            <div className="charts2">
              <div>
                <ExpensePieChart myProp={expenditures}></ExpensePieChart>
              </div>

              <div>
                <ExpensePieChart myProp={weeklyExpenditures}></ExpensePieChart>
              </div>
            </div>
          ) : (
            <div className="charts2">
              <div>
                <h2>Daily Expenditures Visualized</h2>
                <ExpenseBarChart myProp={expenditures}></ExpenseBarChart>
              </div>

              <div>
                <h2>Weekly Expenditures Visualized</h2>
                <ExpenseBarChart myProp={weeklyExpenditures}></ExpenseBarChart>
              </div>
            </div>
          )}
        </div>
        <div className="tables">
          <div className="transactions">
            <h2>Transactions</h2>
            <br />

            <div className="tableporttrans">
              <table
                className="compact-table"
                style={{ border: "1px solid black" }}
                id="transactions"
              >
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {[...transactions].reverse().map((row, index) => (
                    <tr key={index}>
                      <td>{shortenYear(row.Date)}</td>
                      <td>{row.Type}</td>
                      <td>{row.Amount}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="dailyexp">
            <h2>Daily Expenditures</h2>
            <br />

            <div className="tableport">
              <table
                className="compact-table"
                style={{ border: "1px solid black" }}
                id="expenditure"
              >
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Hous.</th>
                    <th>Transp.</th>
                    <th>Food</th>
                    <th>Cloth.</th>
                    <th>Health</th>
                    <th>Pers. Care</th>
                    <th>Edu.</th>
                    <th>Debt</th>
                    <th>Sav./Inv.</th>
                    <th>Entert.</th>
                    <th>Gifts/Don.</th>
                    <th>Misc.</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {[...expenditures].reverse().map((row, index) => (
                    <tr key={index}>
                      <td>{shortenYear(row.Date)}</td>
                      <td>{row.Housing}</td>
                      <td>{row.Transportation}</td>
                      <td>{row.Food}</td>
                      <td>{row.Clothes}</td>
                      <td>{row.Healthcare}</td>
                      <td>{row.PersonalCare}</td>
                      <td>{row.Education}</td>
                      <td>{row.DebtPayments}</td>
                      <td>{row.SavingsInvestments}</td>
                      <td>{row.Entertainment}</td>
                      <td>{row.GiftsDonations}</td>
                      <td>{row.Misc}</td>
                      <td>{row.Total}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="weeklyexp">
            <h2>Weekly Expenditures</h2>
            <br />
            <div className="tableport">
              <table
                className="compact-table"
                style={{ border: "1px solid black" }}
                id="weeklyexpenditure"
              >
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Hous.</th>
                    <th>Transp.</th>
                    <th>Food</th>
                    <th>Cloth.</th>
                    <th>Health</th>
                    <th>Pers. Care</th>
                    <th>Edu.</th>
                    <th>Debt</th>
                    <th>Sav./Inv.</th>
                    <th>Entert.</th>
                    <th>Gifts/Don.</th>
                    <th>Misc.</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {[...weeklyExpenditures].reverse().map((row, index) => (
                    <tr key={index}>
                      <td>{shortenYear(row.Date)}</td>
                      <td>{row.Housing}</td>
                      <td>{row.Transportation}</td>
                      <td>{row.Food}</td>
                      <td>{row.Clothes}</td>
                      <td>{row.Healthcare}</td>
                      <td>{row.PersonalCare}</td>
                      <td>{row.Education}</td>
                      <td>{row.DebtPayments}</td>
                      <td>{row.SavingsInvestments}</td>
                      <td>{row.Entertainment}</td>
                      <td>{row.GiftsDonations}</td>
                      <td>{row.Misc}</td>
                      <td>{row.Total}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
