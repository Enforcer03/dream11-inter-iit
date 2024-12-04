# Product UI

This folder contains the user interface (UI) components and layout designs for the **Product** module of the AI Model Predictor. The UI serves as the interactive layer where users can create and manage their fantasy teams, receive predictive insights, and explore game features.

## Contents

- [Features](#features)
- [Folder Structure](#folder-structure)
- [Technologies Used](#technologies-used)
- [Dependencies](#dependencies)
- [Setup](#how-to-setup)

## Features

- **Team Creation Interface**: Allows users to select players and create fantasy teams.
- **Prediction Visualization**: Displays predictive insights to assist users in building better teams.
- **User-Friendly Design**: Responsive and intuitive design tailored for a seamless gaming experience.
- **Interactive Dashboard**: View team performance and player statistics.

## Folder Structure

```plaintext
UI/
├── app/           # Contains the core application structure
│   ├── api/  # API requests for different functions using axios
│   ├── components/  # Reusable React components for the UI
│   ├── contexts/  # React contexts for state management
│   ├── types/  # Typescript types
│   └── [route]/      # Page-specific layouts and views
├── public/        # Static assets such as images, icons, and logos
```

## Technologies Used

- **React.js**: For building reusable and dynamic user interface components.
- **Next.js**: Framework for server-side rendering and routing.
- **Tailwind CSS**: For efficient and customizable styling.
- **Axios/Fetch**: For API integration to fetch predictive and player data.

## Dependencies

- The only you need for running the UI is [NodeJS](https://nodejs.org/en). Here is the installation guide for all platforms - [Installation Guide](https://nodejs.org/en/download/package-manager)

## How to Setup

1. **Install Yarn** (if not already installed):

- With npm:

  ```bash
    npm install --global yarn
  ```

2. Navigate to the `UI/` folder:

   ```bash
   cd UI
   ```

3. Install the dependencies:

   ```bash
   yarn install
   ```

4. Start the development server:

   ```bash
   yarn dev
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```
