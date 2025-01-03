# FocusPandas: HealthKit and Screen Time Data Analyzer

![FocusPandas Header](https://github.com/AndreasInk/FocusPandas/blob/main/assets/FocusPandas%20header.png)

![FocusPandas Bento](https://github.com/AndreasInk/FocusPandas/blob/main/assets/FocusPandas%20bento.png)

**FocusPandas** is a data visualization and analysis tool that helps you explore and understand your digital habits, health metrics, and productivity patterns. Using Apple Health and Screen Time data, FocusPandas provides insights into how your daily habits influence your productivity, health, and overall well-being.

## Features
- **Screen Time Analysis**: Explore app usage trends, peak usage times, and detailed app statistics. Use this tool to preserve your Screen Time data, ensuring it remains available for long-term analysis, even if your system resets it.
- **Heart Rate Insights**: Correlate heart rate data with screen time and productivity.
- **Sleep Analysis**: Explore the relationship between sleep patterns, productivity, and screen time.
- **Productivity Metrics**: Calculate daily productivity ratios and highlight trends.
- **Additional Insights**: Gain insights into audio exposure, digital habits, and more.


---

## Getting Started

Follow these steps to set up and run the application:

### 1. Clone the Repository
```bash
git clone https://github.com/AndreasInk/FocusPandas.git
cd focuspandas
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python libraries using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Extract Screen Time Data
Run the following command to extract Screen Time data into the `data/` directory:
```bash
sudo python3 extract_db.py
```
This step fetches the Screen Time data from macOS's database and saves it locally, ensuring you have a backup of your digital habits. This is especially useful as macOS only retains Screen Time data for up to 2 months or may reset data during OS updates.

### 5. Export Apple Health Data
Export your Apple Health data from the **Apple Health** app:
1. Open the Apple Health app on iOS.
2. Go to your profile (top right of the app on iOS 18+).
3. Tap **Export All Health Data** (at the bottom of the view).
4. Place the resulting XML file in the `data/` directory.

### 6. Run the Streamlit App
Launch the app using Streamlit:
```bash
streamlit run app.py
```
The app will open in your default web browser. If not, visit [http://localhost:8501](http://localhost:8501).

---

## Application Overview

The app is organized into six main sections, accessible from the sidebar:
1. **Screen Time Analysis**  
   Explore app usage trends, peak usage times, and detailed app statistics.
2. **Heart Rate Analysis**  
   Analyze how heart rate correlates with screen time and digital habits.
3. **Sleep Analysis**  
   Visualize sleep duration trends and how sleep affects productivity and screen usage.
4. **Productivity Analysis**  
   Understand the relationship between productivity, sleep, and audio exposure.
5. **Productivity Metrics**  
   View daily productivity metrics, including usage hours and productivity ratios.
6. **Additional Insights**  
   Gain insights into daily screen time patterns, productivity vs. audio exposure, and more.

---

## Data Sources
- **Screen Time Data**: Extracted directly from your system database.
- **Apple Health Data**: Exported via Apple Health and processed to extract heart rate, sleep, and audio exposure metrics.

---

## Dependencies

The project uses the following Python libraries:
- `streamlit` for creating the interactive web app.
- `pandas` for data processing and analysis.
- `matplotlib` for data visualization.
- `pydantic` for managing structured data.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions would be great! Please feel free to submit a pull request or open an issue.
