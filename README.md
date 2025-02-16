# Patent Q&A Data Management System

A Flask-based web application for managing and generating patent-related Q&A data. This system helps users generate various types of questions based on existing patent Q&A pairs using different expert roles.

## Features

- **Multi-Language Support**
  - Traditional Chinese
  - English
  - Real-time language switching

- **Expert Roles**
  - Concept Query Expert
  - Keyword Query Expert
  - Factual Query Expert
  - Spelling Error Query Expert
  - Web Query Expert

- **Core Functionalities**
  - Upload and manage patent Q&A data
  - Generate new questions based on existing Q&A pairs
  - Search functionality with real-time filtering
  - Export generated Q&A pairs to CSV
  - Save and manage generated questions

- **User Interface**
  - Responsive design for all devices
  - Modern and intuitive interface
  - Real-time search results
  - Dynamic content generation

## Technical Stack

- **Backend**
  - Flask (Python web framework)
  - OpenAI API for question generation
  - Pandas for data handling

- **Frontend**
  - Bootstrap 5 for responsive design
  - JavaScript for dynamic interactions
  - Font Awesome for icons

## Installation

1. Clone the repository:
```bash
git clone https://github.com/renruntao/patent_rag.git
cd patent_rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Configure your OpenAI API key
export OPENAI_API_KEY='your-api-key'
export OPENAI_API_BASE='your-api-base-url'
```

4. Run the application:
```bash
python app.py
```

## Usage

1. **Upload Data**
   - Prepare your patent Q&A data in CSV format
   - Use the upload function to import your data
   - The system will automatically process and display the data

2. **Generate Questions**
   - Select an expert role from the dropdown menu
   - Set the number of questions to generate
   - Click the generate button next to any Q&A pair

3. **Search and Filter**
   - Use the search box to filter Q&A pairs
   - Results update in real-time
   - Highlights matching terms

4. **Export Data**
   - Select the questions you want to save
   - Click the export button to download as CSV

## API Integration

The system integrates with OpenAI's API for question generation. Each expert role has a specific system prompt that guides the AI in generating appropriate questions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue in the GitHub repository.