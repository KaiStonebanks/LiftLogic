# LiftLogic

LiftLogic is a Django web application capable of tracking workout history, establishing powerlifting baselines (1-Rep Max), and calculating personalized 3-week Smolov Jr. routines based on user progression.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd <repo_directory>
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   
   # For Mac/Linux:
   source venv/bin/activate  
   
   # For Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate the Database** (Generates dummy users, profiles, and logs):
   ```bash
   python population_script.py
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## External Sources / Acknowledgements
- **Videos**: The Lifting Guides page embeds tutorials directly sourced from YouTube:
  - Bench Press: `https://www.youtube.com/watch?v=BYKScL2sgCs`
  - Squat: `https://www.youtube.com/watch?v=UFs6E3Ti1jg`
  - Deadlift: `https://www.youtube.com/watch?v=MBbyAqvTNkU`
