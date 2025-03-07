import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import Expenses from "./components/Expenses.jsx";
import ViewExpenses from "./components/ViewExpenses.jsx"; // Import ViewExpenses component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/expenses" element={<Expenses />} />
        <Route path="/view-expenses" element={<ViewExpenses />} /> {/* New Route */}
      </Routes>
    </Router>
  );
}

export default App;
