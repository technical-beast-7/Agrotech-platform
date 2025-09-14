# Agrotech Platform

Agrotech is a comprehensive agricultural platform designed to empower farmers with crop recommendations, market price analysis, a produce marketplace, and innovative land leasing solutions. The platform aims to leverage technology to enhance agricultural productivity and connectivity.

## Features

*   **Land Leasing**: Landowners with underutilized land can seamlessly register their property on our platform, making it visible to farmers who can explore and lease the land for agricultural use.
*   **Crop Recommendation System**: Delivers tailored crop suggestions based on various agronomic parameters.
*   **Market Price Analysis**: Provides real-time insights into prevailing market prices for diverse commodities.
*   **Buy/Sell Marketplace**: Enables direct transactions between farmers for buying and selling produce.
*   **Multilingual Support**: Accessible in English, Hindi, and Marathi to cater to a diverse user base.
*   **Chatbot**: An interactive assistant to address farmer inquiries.
*   **User Authentication**: Robust and secure sign-up/sign-in functionalities.
*   **User Profiles**: Personalized dashboards for farmers to manage their information, listings, and leased land.
*   **News and Trends**: Keeps users informed with the latest agricultural developments and trends.

## Technologies Used

*   **Backend**: Python (Flask Framework)
*   **Frontend**: HTML, CSS, JavaScript
*   **Database**: (Implicitly, likely SQLite or similar for local development, or a more robust one for deployment)
*   **Machine Learning**: Scikit-learn (for crop recommendation models)
*   **Web Server**: Waitress (for local development/testing)
*   **Data Analysis**: Pandas, NumPy

## Setup Instructions

To set up the project locally, follow these steps:

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/technical-beast-7/Agrotech-platform
    cd Agrotech-platform
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:

    ```bash
    waitress-serve --listen=0.0.0.0:5000 fixed_app:app
    ```

    The application will be accessible at `http://localhost:5000`.

## Project Structure

*   `fixed_app.py`: Main Flask application file.
*   `crops.py`: Python script related to crop data.
*   `templates/`: Contains all HTML template files for the web interface, including land leasing pages and forms.
*   `static/`: Contains static assets like CSS, JavaScript, and images.
*   `requirements.txt`: Lists all Python dependencies.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
