import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API_URL = `${API_BASE_URL}/api/munsoon/analyze`;
const COMPARE_URL = `${API_BASE_URL}/api/munsoon/compare`;

function App() {
  const [result, setResult] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  const [batterySoc, setBatterySoc] = useState(50);
  const [batteryCapacity, setBatteryCapacity] = useState(5);
  const [gridAvailable, setGridAvailable] = useState(false);

  // Prototype monsoon scenario
  const solarGeneration = [
    0,
    0,
    0,
    0,
    0,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.35,
    0.30,
    0.20,
    0.15,
    0.08,
    0.03,
    0,
    0,
    0,
    0,
    0,
  ];

  const householdDemand = [
    0.30,
    0.30,
    0.30,
    0.30,
    0.50,
    0.70,
    0.60,
    0.50,
    0.30,
    0.30,
    0.30,
    0.30,
    0.30,
    0.30,
    0.30,
    0.40,
    0.60,
    0.80,
    1.00,
    0.80,
    0.60,
    0.50,
    0.40,
    0.30,
  ];

  // --------------------------------
  // ENERGY ANALYSIS
  // --------------------------------

  const hourlyEnergyData = solarGeneration.map(
  (solar, index) => ({
    hour: `${String(index).padStart(2, "0")}:00`,
    solar: solar,
    demand: householdDemand[index],
    })
  );

  const analyzeEnergy = async () => {
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          solar_generation: solarGeneration,
          household_demand: householdDemand,
          battery_capacity_kwh: Number(batteryCapacity),
          battery_soc: Number(batterySoc),
          grid_available: gridAvailable,
        }),
      });

      if (!response.ok) {
        throw new Error("Energy analysis failed");
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);

      alert(
        "Could not connect to MUNSOON backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------
  // REACTIVE VS MUNSOON
  // --------------------------------

  const loadComparison = async () => {
    try {
      const response = await fetch(COMPARE_URL);

      if (!response.ok) {
        throw new Error("Comparison request failed");
      }

      const data = await response.json();

      setComparison(data.comparison);
    } catch (error) {
      console.error("Comparison error:", error);
    }
  };

  // Load comparison when page opens
  useEffect(() => {
    loadComparison();
  }, []);

  // --------------------------------
  // CHART DATA
  // --------------------------------

  const shortageChartData = comparison
    ? [
        {
          strategy: "Reactive",
          shortage: comparison.reactive.shortage_kwh,
        },
        {
          strategy: "MUNSOON",
          shortage: comparison.munsoon.shortage_kwh,
        },
      ]
    : [];

  const coverageChartData = comparison
    ? [
        {
          strategy: "Reactive",
          coverage:
            comparison.reactive.energy_coverage_percent,
        },
        {
          strategy: "MUNSOON",
          coverage:
            comparison.munsoon.energy_coverage_percent,
        },
      ]
    : [];

  // --------------------------------
  // UI
  // --------------------------------

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      <div className="max-w-6xl mx-auto">

        {/* HEADER */}

        <header className="mb-10">

          <div className="flex items-center gap-3">

            <div className="text-4xl">
              ☁️
            </div>

            <div>

              <h1 className="text-4xl font-bold tracking-tight">
                MUNSOON
              </h1>

              <p className="text-slate-400">
                AI-Powered Energy Resilience for
                Monsoon-Prone Solar Homes
              </p>

            </div>

          </div>

        </header>


        {/* MAIN QUESTION */}

        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-8 mb-6">

          <p className="text-slate-400 text-sm uppercase tracking-widest mb-3">
            Energy Resilience Check
          </p>

          <h2 className="text-3xl font-bold mb-2">
            Will my house make it through tonight?
          </h2>

          <p className="text-slate-500 text-sm mb-8">
            Prototype simulation • Forecast values are simulated
          </p>


          <div className="grid md:grid-cols-3 gap-6">

            {/* Battery Capacity */}

            <div>

              <label className="text-sm text-slate-400">
                Battery Capacity (kWh)
              </label>

              <input
                type="number"
                value={batteryCapacity}
                onChange={(e) =>
                  setBatteryCapacity(e.target.value)
                }
                className="w-full mt-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3"
              />

            </div>


            {/* Battery SOC */}

            <div>

              <label className="text-sm text-slate-400">
                Current Battery %
              </label>

              <input
                type="number"
                min="0"
                max="100"
                value={batterySoc}
                onChange={(e) =>
                  setBatterySoc(e.target.value)
                }
                className="w-full mt-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3"
              />

            </div>


            {/* Grid */}

            <div>

              <label className="text-sm text-slate-400">
                Grid Status
              </label>

              <button
                onClick={() =>
                  setGridAvailable(!gridAvailable)
                }
                className={`w-full mt-2 rounded-xl px-4 py-3 font-semibold ${
                  gridAvailable
                    ? "bg-emerald-600"
                    : "bg-red-600"
                }`}
              >
                {gridAvailable
                  ? "GRID AVAILABLE"
                  : "GRID OUTAGE"}
              </button>

            </div>

          </div>


          {/* ANALYZE BUTTON */}

          <button
            onClick={analyzeEnergy}
            disabled={loading}
            className="mt-8 w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 rounded-xl py-4 font-bold text-lg transition"
          >
            {loading
              ? "Analyzing Energy Situation..."
              : "Analyze Energy Risk"}
          </button>

        </section>


        {/* RESULTS */}

        {result && (
          <>

            {/* METRICS */}

            <section className="grid md:grid-cols-4 gap-4 mb-6">

              <Metric
                title="Expected Solar"
                value={`${result.analysis.total_solar_kwh} kWh`}
              />

              <Metric
                title="Expected Demand"
                value={`${result.analysis.total_demand_kwh} kWh`}
              />

              <Metric
                title="Energy Coverage"
                value={`${result.analysis.energy_coverage_percent}%`}
              />

              <Metric
                title="Battery Remaining"
                value={`${result.analysis.final_battery_soc_percent}%`}
              />

            </section>


            {/* RISK ASSESSMENT */}

            <section className="bg-slate-900 border border-slate-800 rounded-3xl p-8 mb-6">

              <p className="text-slate-400 text-sm uppercase tracking-widest">
                MUNSOON Assessment
              </p>


              <div className="flex items-center justify-between mt-3">

                <h2 className="text-4xl font-bold">
                  {result.agent.risk} RISK
                </h2>

                <div className="text-5xl">

                  {result.agent.risk === "HIGH"
                    ? "🔴"
                    : result.agent.risk === "MEDIUM"
                    ? "🟡"
                    : "🟢"}

                </div>

              </div>


              <p className="text-slate-300 mt-5 text-lg leading-relaxed">
                {result.agent.reason}
              </p>


              {/* RECOMMENDED ACTIONS */}

              <div className="mt-6 bg-slate-800 rounded-2xl p-5">

                <h3 className="font-bold text-xl mb-4">
                  Recommended Actions
                </h3>

                <ul className="space-y-3">

                  {result.agent.recommended_actions.map(
                    (action, index) => (

                      <li
                        key={index}
                        className="flex gap-3 text-slate-300"
                      >

                        <span className="text-emerald-400">
                          ✓
                        </span>

                        {action}

                      </li>

                    )
                  )}

                </ul>

              </div>

            </section>

            {/* 24-HOUR ENERGY PROFILE */}

<section className="bg-slate-900 border border-slate-800 rounded-3xl p-8 mb-6">

  <div className="flex items-center justify-between mb-2">

    <div>

      <h2 className="text-2xl font-bold">
        24-Hour Energy Profile
      </h2>

      <p className="text-slate-400 mt-1">
        Solar generation vs expected household demand
      </p>

    </div>

    <div className="text-3xl">
      ☀️
    </div>

  </div>


  <p className="text-slate-500 text-sm mb-8">
    Monsoon prototype scenario • Values represent estimated
    hourly energy availability and household demand.
  </p>


  <div className="w-full h-80">

    <ResponsiveContainer
      width="100%"
      height="100%"
    >

      <LineChart
        data={hourlyEnergyData}
        margin={{
          top: 10,
          right: 20,
          left: 10,
          bottom: 10,
        }}
      >

        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#334155"
        />

        <XAxis
          dataKey="hour"
          stroke="#94a3b8"
          interval={2}
        />

        <YAxis
          stroke="#94a3b8"
          label={{
            value: "Energy (kWh)",
            angle: -90,
            position: "insideLeft",
            fill: "#94a3b8",
          }}
        />

        <Tooltip />

        <Legend />

        <Line
          type="monotone"
          dataKey="solar"
          name="Solar Generation"
          stroke="#facc15"
          strokeWidth={3}
          dot={false}
        />

        <Line
          type="monotone"
          dataKey="demand"
          name="Household Demand"
          stroke="#60a5fa"
          strokeWidth={3}
          dot={false}
        />

      </LineChart>

    </ResponsiveContainer>

  </div>


  <div className="grid md:grid-cols-2 gap-4 mt-6">

    <div className="bg-slate-800 rounded-2xl p-5">

      <p className="text-slate-400 text-sm">
        Daytime Insight
      </p>

      <p className="text-slate-200 mt-2">
        Solar generation rises during daylight hours but
        remains limited in this monsoon scenario.
      </p>

    </div>


    <div className="bg-slate-800 rounded-2xl p-5">

      <p className="text-slate-400 text-sm">
        Evening Risk
      </p>

      <p className="text-slate-200 mt-2">
        Household demand increases as solar generation
        falls, increasing dependence on stored energy.
      </p>

    </div>

  </div>

</section>
            {/* REACTIVE VS MUNSOON */}

            {comparison && (

              <section className="bg-slate-900 border border-slate-800 rounded-3xl p-8 mb-6">

                <div className="flex items-center justify-between mb-2">

                  <div>

                    <h2 className="text-2xl font-bold">
                      Reactive vs MUNSOON
                    </h2>

                    <p className="text-slate-400 mt-1">
                      Controlled prototype simulation
                    </p>

                  </div>

                  <div className="text-3xl">
                    ⚡
                  </div>

                </div>


                <p className="text-slate-500 text-sm mb-8">
                  Same low-generation and grid-outage
                  scenario, compared across two energy
                  management strategies.
                </p>


                {/* SHORTAGE CHART */}

                <div className="mb-10">

                  <h3 className="font-semibold text-lg mb-4">
                    Estimated Energy Shortage
                  </h3>

                  <div className="w-full h-72">

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <BarChart
                        data={shortageChartData}
                      >

                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke="#334155"
                        />

                        <XAxis
                          dataKey="strategy"
                          stroke="#94a3b8"
                        />

                        <YAxis
                          stroke="#94a3b8"
                          label={{
                            value: "Shortage (kWh)",
                            angle: -90,
                            position: "insideLeft",
                            fill: "#94a3b8",
                          }}
                        />

                        <Tooltip />

                        <Bar
                          dataKey="shortage"
                          name="Energy Shortage"
                          fill="#ef4444"
                          radius={[8, 8, 0, 0]}
                        />

                      </BarChart>

                    </ResponsiveContainer>

                  </div>

                </div>


                {/* COVERAGE CHART */}

                <div>

                  <h3 className="font-semibold text-lg mb-4">
                    Household Energy Coverage
                  </h3>

                  <div className="w-full h-72">

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <BarChart
                        data={coverageChartData}
                      >

                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke="#334155"
                        />

                        <XAxis
                          dataKey="strategy"
                          stroke="#94a3b8"
                        />

                        <YAxis
                          domain={[0, 100]}
                          stroke="#94a3b8"
                          label={{
                            value: "Coverage (%)",
                            angle: -90,
                            position: "insideLeft",
                            fill: "#94a3b8",
                          }}
                        />

                        <Tooltip />

                        <Bar
                          dataKey="coverage"
                          name="Energy Coverage"
                          fill="#22c55e"
                          radius={[8, 8, 0, 0]}
                        />

                      </BarChart>

                    </ResponsiveContainer>

                  </div>

                </div>


                {/* IMPACT NUMBERS */}

                <div className="grid md:grid-cols-2 gap-4 mt-8">

                  <div className="bg-slate-800 rounded-2xl p-5">

                    <p className="text-slate-400 text-sm">
                      Shortage Reduction
                    </p>

                    <p className="text-3xl font-bold mt-2">
                      {comparison.shortage_reduction_kwh} kWh
                    </p>

                  </div>


                  <div className="bg-slate-800 rounded-2xl p-5">

                    <p className="text-slate-400 text-sm">
                      Coverage Improvement
                    </p>

                    <p className="text-3xl font-bold mt-2">

                      +
                      {
                        comparison.coverage_improvement_percentage_points
                      }

                      <span className="text-xl ml-1">
                        pp
                      </span>

                    </p>

                  </div>

                </div>

              </section>

            )}


            {/* RAG */}

            <section className="bg-slate-900 border border-slate-800 rounded-3xl p-8">

              <h2 className="text-2xl font-bold mb-2">
                AI Reasoning Context
              </h2>

              <p className="text-slate-400 mb-6">
                Knowledge retrieved by the MUNSOON RAG system
              </p>


              <div className="grid md:grid-cols-3 gap-4">

                {result.agent.retrieved_knowledge.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="bg-slate-800 rounded-2xl p-5"
                    >

                      <h3 className="font-semibold capitalize mb-3">
                        {item.topic.replaceAll("_", " ")}
                      </h3>

                      <p className="text-slate-400 text-sm leading-relaxed">
                        {item.content}
                      </p>

                    </div>

                  )
                )}

              </div>

            </section>


            {/* DISCLAIMER */}

            <p className="text-center text-slate-500 text-sm mt-6 mb-8">

              Prototype simulation — predictions are
              estimates and do not guarantee uninterrupted
              electricity.

            </p>

          </>
        )}

      </div>

    </div>
  );
}


// --------------------------------
// METRIC COMPONENT
// --------------------------------

function Metric({ title, value }) {

  return (

    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

      <p className="text-slate-400 text-sm">
        {title}
      </p>

      <p className="text-2xl font-bold mt-2">
        {value}
      </p>

    </div>

  );
}


export default App;