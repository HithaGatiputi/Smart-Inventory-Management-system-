import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {

  const [forecast, setForecast] = useState(null);

  const runForecast = async () => {

    const response = await axios.post(
      'http://localhost:8000/api/predict',
      {
        product: 'Sugar',
        category: 'Staples',
        units_sold: 40,
        current_stock: 120,
        days_remaining: 3,
        rain: true,
        salary_week: true,
        ipl_match: false,
        festival: 'Diwali',
        area_type: 'family'
      }
    );

    setForecast(response.data);
  };

  return (
    <div style={{ padding: 20 }}>

      <h1>Kirana AI Dashboard</h1>

      <button onClick={runForecast}>
        Run Forecast
      </button>

      {forecast && (

        <div>

          <h2>Forecast Result</h2>

          <pre>
            {JSON.stringify(forecast, null, 2)}
          </pre>

        </div>
      )}

    </div>
  );
}