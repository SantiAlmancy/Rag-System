const API_URL = "http://127.0.0.1:8000";


export const askFormula1 = async (question, text) => {
  try {
    const response = await fetch(`${API_URL}/generate-answer/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question, text }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      if (errorData.value) {
        return errorData;
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};