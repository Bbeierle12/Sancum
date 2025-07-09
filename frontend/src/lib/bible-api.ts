
import axios from 'axios';

const BIBLE_API_URL = 'https://bible-api.com';

export async function getVerse(reference: string) {
  try {
    const response = await axios.get(`${BIBLE_API_URL}/${reference}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching verse:', error);
    return null;
  }
}
