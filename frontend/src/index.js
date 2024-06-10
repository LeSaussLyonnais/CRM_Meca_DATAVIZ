import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { SiteProvider } from './Components/ContexteSelectionSite';


import App from "./App";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <SiteProvider>

      <App />
    </SiteProvider>

  </StrictMode>
);
