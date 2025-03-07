import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./ViewExpenses.css";

export default function ViewExpenses() {
  const [expenses, setExpenses] = useState([]);
  const [editingExpense, setEditingExpense] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    if (!username) {
      alert("User not logged in");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/search_data/${username}`);
      if (!response.ok) {
        throw new Error("Failed to fetch expenses");
      }
      const data = await response.json();
      setExpenses(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleDelete = async (username) => {
    try {
      const response = await fetch(`${API_BASE_URL}/delete_data/${username}`, {
        method: "DELETE",
      });
  
      if (!response.ok) {
        throw new Error("Failed to delete expense");
      }
  
      alert("Expense deleted successfully!");
  
      // ✅ Remove deleted record from state
      setExpenses(expenses.filter(expense => expense.username !== username));
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to delete expense.");
    }
  };
  

  const handleEdit = (expense) => {
    setEditingExpense({ ...expense });
  };

  const handleUpdate = async () => {
    if (!editingExpense) return;

    try {
      const response = await fetch(`${API_BASE_URL}/edit_expenses/${editingExpense.username}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingExpense),
      });

      if (!response.ok) {
        throw new Error("Failed to update expense");
      }

      alert("Expense updated successfully!");
      setEditingExpense(null);
      fetchExpenses();
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to update expense.");
    }
  };

  return (
    <div className="view-expenses-container">
      <h2>All Expenses</h2>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr key={expense.username}>
              {editingExpense?.username === expense.username ? (
                <>
                  <td>
                    <input
                      type="text"
                      name="category"
                      value={editingExpense.category}
                      onChange={(e) => setEditingExpense({ ...editingExpense, category: e.target.value })}
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      name="amount"
                      value={editingExpense.amount}
                      onChange={(e) => setEditingExpense({ ...editingExpense, amount: e.target.value })}
                    />
                  </td>
                  <td>
                    <input
                      type="date"
                      name="date"
                      value={editingExpense.date}
                      onChange={(e) => setEditingExpense({ ...editingExpense, date: e.target.value })}
                    />
                  </td>
                  <td>
                    <button onClick={handleUpdate}>Save</button>
                    <button onClick={() => setEditingExpense(null)}>Cancel</button>
                  </td>
                </>
              ) : (
                <>
                  <td>{expense.category}</td>
                  <td>{expense.amount}</td>
                  <td>{expense.date}</td>
                  <td>
                    <button onClick={() => handleEdit(expense)}>Edit</button>
                    <button onClick={() => handleDelete(expense.username)}>Delete</button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Back to Expenses Page */}
      <button className="back-button" onClick={() => navigate("/expenses")}>
        Back to Expenses
      </button>
    </div>
  );
}
