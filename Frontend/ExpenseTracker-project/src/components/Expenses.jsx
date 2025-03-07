import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Expenses.css";

export default function Expenses() {
  const [expenseData, setExpenseData] = useState({
    category: "",
    amount: "",
    date: "",
  });

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setExpenseData({ ...expenseData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!username) {
      alert("User not logged in");
      return;
    }
  
    const expenseDataToSend = {
      username, // ✅ Include username in request payload
      amount: expenseData.amount,
      category: expenseData.category,
      date: expenseData.date,
    };
  
    try {
      const response = await fetch(`${API_BASE_URL}/save_expenses/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(expenseDataToSend),
      });
  
      if (!response.ok) {
        throw new Error("Failed to save expense");
      }
  
      alert("Expense saved successfully!");
      setExpenseData({ category: "", amount: "", date: "" }); // Reset form
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to save expense.");
    }
  };
  

  return (
    <div className="expenses-container">
      <h2>Submit Expense</h2>
      <form onSubmit={handleSubmit} className="expenses-form">
        <select name="category" value={expenseData.category} onChange={handleChange} required>
          <option value="">Select Category</option>
          <option value="Food">Food</option>
          <option value="Entertainment">Entertainment</option>
          <option value="Groceries">Groceries</option>
          <option value="Bills">Bills</option>
          <option value="Medical">Medical</option>
        </select>
        <input
          type="number"
          name="amount"
          placeholder="Amount"
          value={expenseData.amount}
          onChange={handleChange}
          required
        />
        <input type="date" name="date" value={expenseData.date} onChange={handleChange} required />
        <button type="submit">Submit Expense</button>
      </form>

      {/* View Expenses Button */}
      <button className="view-expenses-button" onClick={() => navigate("/view-expenses")}>
        View Expenses
      </button>
    </div>
  );
}
