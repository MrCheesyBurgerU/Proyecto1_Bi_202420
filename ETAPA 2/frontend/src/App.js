import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/NavBar";
import TextPrediction from "./components/TextPrediction";
import CsvPrediction from "./components/CsvPrediction";
import ImportantWords from "./components/ImportantWords";
import Model from "./components/Model";

const App = () => {

	return (
		<Router>
			<div>
				<NavBar />
				<Routes>
					<Route path="/text" element={<TextPrediction />} />
					<Route path="/csv" element={<CsvPrediction />} />
					<Route path="/" element={<TextPrediction />} />
					<Route path="/words" element={<ImportantWords />} />
					<Route path="/model" element={<Model />} />
				</Routes>
			</div>
		</Router>
	);
};



export default App;
