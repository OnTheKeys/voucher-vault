import { BrowserRouter, Routes, Route } from "react-router"
import './App.css'
import FormFill from './Pages/file'
import ThankYou from "./Pages/thankyou"
import { Provider } from './components/ui/provider'

function AppContent() {

  return (
    <>
      <Routes>
        <Route path="/form" element={<FormFill />} />
        <Route path="/order-placed" element={<ThankYou />} />
      </Routes>
    </>
  );
}
function App() {
  return (
    <Provider>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
    </Provider>
  )
}

export default App
