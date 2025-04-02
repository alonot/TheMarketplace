import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import BrowseCategory from "./components/categories";
import { categorieslist } from "./components/categories";
import App from "next/app";

const root = createRoot(document.getElementById("root"));
root.render(
    <StrictMode>
        <App/>
    </StrictMode>
);