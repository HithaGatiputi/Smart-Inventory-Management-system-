
import { useState } from 'react';
import axios from 'axios';

export default function ScenarioSimulator() {

  const [result, setResult] = useState(null);

  const runScenario = async () => {

    const response = await axios.post(
      'http://localhost:8000/api/predict',
      {
        product: 'Sugar',
        units_sold: 40,
        rain: true,
        festival: 'Diwali'
      }
    );

    setResult(response.data);
  };

  return (
    <div>
      <button onClick={runScenario}>
        Run Scenario
      </button>

      {result && (
        <pre>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
