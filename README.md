# Stayabucks

Stayabucks is a versatile web application designed to let you create and personalize your favorite Starbucks drinks.
With Stayabucks, you can recreate the Starbucks experience by personalizing every detail of your coffee, exactly the way
you want it.

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
    - [Running the Api Locally](#running-the-api-locally)
    - [Running the web app Locally](#running-the-web-app-locally)
- [How to Use](#how-to-use)
- [Contributing](#contributing)
- [Contributor](#contributor)
- [License](#license)

## Demo

- **[Coming Soon]** - https://stayabucks.coding-project.fr/

## Features

- [ ] Authentication
- [ ] Menu visualization
- [ ] Create customized drinks
- [ ] Search for existing drinks
- [ ] Drink rating system
- [ ] Database updating
- [ ] Classification of drink by various criteria
- [ ] Online payment integration

## Requirements

To run the Stayabucks API and web application, you'll need the following software and tools:

1. **Python 3.10**: Python is used for the FastAPI application. You can download Python 3.10 from the official website:

    - [Download Python 3.10 for Windows and macOS](https://www.python.org/downloads/release/python-3100/)

2. **Docker**: Docker is required to run the database using Docker Compose. You can download Docker from the official
   website:

    - [Download Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Download Docker for macOS](https://docs.docker.com/desktop/install/mac-install/)

3. **Postman (Optional)**: Postman is a helpful tool for testing API endpoints, but it's optional. You can download
   Postman from the official website:

    - [Download Postman for Windows and macOS](https://www.postman.com/downloads/)

## Getting Started

### Running the Api Locally

To run Api locally on your machine, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AyaAid/Stayabucks.git
    ```
2. **Navigate to the Project Directory**

   ```bash
   cd Stayabucks/api
    ```

3. **Install all modules**

   ```bash
   pip install -r requirements.txt
    ```

4. **Run the database**

   ```bash
   make start-db
    ```
   or
   ```bash
    docker-compose -f dev/docker-compose.yml --env-file .env up --build --detach
     ```

5. **Run the Server**

   ```bash
   uvicorn main:app --reload
    ```

6. **Open Your Browser**

   Visit http://127.0.0.1:8000/, http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc in your web browser to use
   the api. You can also use Postman to test the api.

### Running the web app Locally

To run the Nuxt.js web application located in the "web" directory, follow these steps:

1. **Navigate to the Project Directory**

   ```bash
   cd Stayabucks/web
    ```

2. **Install all modules**

   ```bash
   npm install
    ```

3. **Run the Server**

   ```bash
   npm run dev
    ```

4. **Open Your Browser**

   Visit http://localhost:3000/ to access the Stayabucks Nuxt.js web application.

## How to Use

1. Open Postman.

2. Create a new request by clicking the "New" button.

3. Set the request type to the HTTP method you want to test (e.g., GET).

4. Enter the URL of your FastAPI app, for example, http://localhost:8000.

5. Click the "Send" button to make the request.

6. You should receive a response from your FastAPI application in the Postman interface.

7. You can also test POST, PUT, DELETE, or any other HTTP methods by creating new requests in Postman and setting the
   appropriate request type and data.

## Reporting Issues

If you encounter any issues, bugs, or have suggestions for improvements, please report them on
the [GitHub Issues page](https://github.com/AyaAid/Stayabucks/issues) of this project.

## Contributing

Contributions to this Api project are welcome! If you find any issues or have ideas for improvements, please
open an issue or submit a pull request.

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them with descriptive commit messages.

4. Push your changes to your fork.

5. Open a pull request to the main branch of the original repository.

## Contributor

| ![AyaAid](https://avatars.githubusercontent.com/u/113529159?s=128&v=4) | ![celianloisel](https://avatars.githubusercontent.com/u/77807956?s=128&v=4) | ![Romjah](https://avatars.githubusercontent.com/u/113473758?s=128&v=4) | ![ArKZbeb](https://avatars.githubusercontent.com/u/116552625?s=128&v=4) |
|:----------------------------------------------------------------------:|:---------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:-----------------------------------------------------------------------:|
|                  [AyaAid](https://github.com/AyaAid/)                  |              [celianloisel](https://github.com/celianloisel/)               |                  [Romjah](https://github.com/Romjah/)                  |                 [ArKZbeb](https://github.com/ArKZbeb/)                  |

## License

Stayabucks is open-source software licensed under the [MIT License](LICENSE). Feel free to use, modify, and
distribute the code for your purposes.

### Enjoy the app, and happy coding! 🎮💻
