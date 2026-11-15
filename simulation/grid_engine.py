
import random
from datetime import datetime


class GridSimulationEngine:
    """
    GridShield AI - Simulated Smart Grid Telemetry Engine.
    All generated values are synthetic, not physical measurements.
    """

    def __init__(self):
        self.tick = 0
        self.nominal_voltage = 11.0
        self.nominal_frequency = 50.0
        self.previous_reading = None
        self.rng = random.Random()

    def generate_reading(self, scenario="NORMAL"):

        self.tick += 1

        voltage = self.nominal_voltage + self.rng.uniform(-0.15, 0.15)
        current = self.rng.uniform(180, 250)
        frequency = self.nominal_frequency + self.rng.uniform(-0.04, 0.04)
        temperature = self.rng.uniform(55, 68)
        power_factor = 0.92

        switching_event = False
        communication_status = "ONLINE"

        # Simulated abnormal scenarios
        if scenario == "OVERLOAD":
            current = self.rng.uniform(410, 470)
            temperature = self.rng.uniform(85, 100)

        elif scenario == "VOLTAGE_SAG":
            voltage = self.rng.uniform(8.5, 9.5)

        elif scenario == "FREQUENCY_DEVIATION":
            frequency = self.rng.uniform(48.5, 49.0)

        elif scenario == "UNUSUAL_CONSUMPTION":
            current = self.rng.uniform(330, 390)

        elif scenario == "ABNORMAL_SWITCHING":
            switching_event = True

        elif scenario == "COMMUNICATION_ANOMALY":
            communication_status = "DEGRADED"

        # Smooth electrical parameter transitions
        if self.previous_reading is not None:

            alpha = 0.25

            voltage = (
                self.previous_reading["voltage"]
                + alpha * (voltage - self.previous_reading["voltage"])
            )

            current = (
                self.previous_reading["current"]
                + alpha * (current - self.previous_reading["current"])
            )

            frequency = (
                self.previous_reading["frequency"]
                + alpha * (frequency - self.previous_reading["frequency"])
            )

            temperature = (
                self.previous_reading["temperature"]
                + alpha * (temperature - self.previous_reading["temperature"])
            )

        self.previous_reading = {
            "voltage": voltage,
            "current": current,
            "frequency": frequency,
            "temperature": temperature
        }

        # Three-phase approximate active power in MW
        power = (
            1.732 * voltage * current * power_factor / 1000
        )

        # Simulated transformer load percentage
        load = (current / 350) * 100

        return {
            "timestamp": datetime.now(),
            "tick": self.tick,
            "scenario": scenario,
            "voltage_kv": round(voltage, 2),
            "current_a": round(current, 2),
            "frequency_hz": round(frequency, 2),
            "power_mw": round(power, 2),
            "load_percent": round(load, 2),
            "transformer_temp_c": round(temperature, 2),
            "breaker_status": "CLOSED",
            "switching_event": switching_event,
            "communication_status": communication_status,
            "simulated": True
        }


if __name__ == "__main__":

    engine = GridSimulationEngine()

    print("\nGRIDSHIELD AI - LIVE GRID SIMULATION")
    print("=" * 45)

    for scenario in ["NORMAL", "OVERLOAD", "VOLTAGE_SAG"]:

        reading = engine.generate_reading(scenario)

        print(f"\nScenario: {scenario}")

        for key, value in reading.items():
            print(f"{key}: {value}")

    print("\nSimulation test completed!")
