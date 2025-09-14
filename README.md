# Agrotech Platform

Agrotech is a comprehensive agricultural platform designed to assist farmers with crop recommendations, market price analysis, and a marketplace for buying and selling produce. The platform aims to leverage technology to empower farmers and improve agricultural practices.

## Features

*   **Crop Recommendation System**: Provides recommendations for suitable crops based on various parameters.
*   **Market Price Analysis**: Offers insights into current market prices for different commodities.
*   **Buy/Sell Marketplace**: A platform for farmers to buy and sell their produce directly.
*   **Multilingual Support**: Available in English, Hindi, and Marathi for broader accessibility.
*   **Chatbot**: An interactive chatbot to answer farmer queries.
*   **User Authentication**: Secure sign-up and sign-in functionalities.
*   **User Profiles**: Personalized profiles for farmers to manage their information and listings.
*   **News and Trends**: Keeps users updated with the latest agricultural news and trends.

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
*   `templates/`: Contains all HTML template files for the web interface.
*   `static/`: Contains static assets like CSS, JavaScript, and images.
*   `requirements.txt`: Lists all Python dependencies.

## Contributing


Contributions are welcome! Please fork the repository and create a pull request with your changes.



