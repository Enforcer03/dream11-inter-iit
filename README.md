<img src="d11_logo.png" width="200">

# **AI Team Builder - Inter IIT 13.0**


## **Setup Instructions**
Setup video in `docs/`.

### 1. **Create and Activate Python Virtual Environment**
```bash
python -m venv env
source env/bin/activate
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Running the APIs and UI**

### **Run Model API**
1. Navigate to the `model/` directory:
   ```bash
   cd model
   ```
2. Start the Model API:
   ```bash
   python model_API.py
   ```

### **Run Squads API**
1. Open a new terminal with the same virtual environment activated.
2. Run the Squads API:
   ```bash
   python Squads_API.py
   ```

### **Run Aggregate Stats API**
1. Open a new terminal with the same virtual environment activated.
2. Run the Aggregate Stats API:
   ```bash
   python Aggregate_stats_API.py
   ```

### **Run Streamlit App**
1. Open a new terminal with the same virtual environment activated.
2. Navigate to the `model/` directory:
   ```bash
   cd model
   ```
3. Start the Streamlit app:
   ```bash
   streamlit run app1.py
   ```

---

## **Running the Product UI**

### 1. **Install Yarn** (if not already installed):
```bash
npm install --global yarn
```

### 2. **Navigate to the `UI/` Folder**
```bash
cd UI
```

### 3. **Install Dependencies**
```bash
yarn install
```

### 4. **Start the Development Server**
```bash
yarn dev
```

### 5. **Access the UI**
Open your browser and navigate to:
```
http://localhost:3000
```

---

## **Directory Structure**

- `model/`: Contains all the logic for the methodology implemented and other experiments.
- `data_preprocessing/`: Handles data cleaning, transformation, and preparation.
- `UI/`: Contains the Product UI providing an interactive experience to predict the optimal team.

---

## **Dependencies**

Ensure you have the following installed:
- Python (version specified in `requirements.txt`)
- Node.js (latest stable version)
- Yarn (latest stable version)

---

## **How to Run the Product UI?**
Refer to the [`Product UI README`](./UI/README.md) for detailed instructions.

Steps (summary):
1. Install Yarn if not already installed:
   ```bash
   npm install --global yarn
   ```
2. Navigate to the `UI/` folder:
   ```bash
   cd UI
   ```
3. Install dependencies:
   ```bash
   yarn install
   ```
4. Start the development server:
   ```bash
   yarn dev
   ```
5. Access the UI in your browser at:
   ```
   http://localhost:3000
   ```

---

## **How to Run the Model UI?**
Refer to the [`Model README`](./model/README.md) for detailed instructions.

---

## **Preprocessing**
Refer to the [`Data Preprocessing README`](./data_preprocessing/README.md) for instructions on data preprocessing.
