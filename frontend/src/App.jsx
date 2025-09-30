/**
 * App.jsx
 * ----------------
 * Root app component.
 * - Wraps the app in AppProvider (context)
 * - Renders Home page
 */

import { AppProvider } from "./context/AppContext";
import Home from "./pages/Home";
import "./styles/globals.css";

function App() {
    return (
        <AppProvider>
            <div className="min-h-screen bg-gray-50">
                <Home />
            </div>
        </AppProvider>
    );
}

export default App;
