import { writable } from 'svelte/store';
import { authStore } from './auth';

export interface ChatMessage {
  sender: 'Student' | 'Psychologist';
  content: string;
}

// Store для истории чата психолога
export const psychologistChatStore = writable<ChatMessage[]>([]);
export const isLoadingPsychologistStore = writable<boolean>(false);

// Инициализация истории чата психолога с приветственным сообщением
export function initPsychologistChat(): void {
  psychologistChatStore.set([
    {
      sender: 'Psychologist',
      content: 'Привет! Я виртуальный психолог. Я здесь, чтобы выслушать тебя и помочь разобраться с любыми проблемами, которые тебя беспокоят. Расскажи, что тебя тревожит или о чем бы ты хотел(а) поговорить сегодня?'
    }
  ]);
}

// Отправка сообщения психологическому ИИ
export async function sendMessageToPsychologist(message: string): Promise<string | null> {
  try {
    isLoadingPsychologistStore.set(true);
    
    // Добавляем сообщение пользователя в историю чата
    const userMessage: ChatMessage = {
      sender: 'Student',
      content: message
    };
    
    psychologistChatStore.update(history => [...history, userMessage]);
    
    // Задержка имитации обработки (в реальном приложении здесь будет API запрос)
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Здесь будет ваш реальный API-запрос к серверу
    // Пока просто имитация ответа психолога
    const psychologistResponse = generatePsychologistResponse(message);
    
    // Добавление ответа психолога в историю чата
    const psychologistMessage: ChatMessage = {
      sender: 'Psychologist',
      content: psychologistResponse
    };
    
    psychologistChatStore.update(history => [...history, psychologistMessage]);
    
    return psychologistResponse;
  } catch (error) {
    console.error('Error sending message to psychologist:', error);
    return null;
  } finally {
    isLoadingPsychologistStore.set(false);
  }
}

// Очистка истории чата психолога
export function clearPsychologistChat(): void {
  psychologistChatStore.set([]);
  initPsychologistChat();
}

// Симуляция ответа психолога (в реальном приложении будет заменено на API)
function generatePsychologistResponse(message: string): string {
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('стресс') || lowerMessage.includes('тревога') || lowerMessage.includes('беспокойство')) {
    return 'Я понимаю, что ты испытываешь тревогу. Это совершенно нормальная реакция на сложные ситуации. Давай обсудим, что именно вызывает у тебя стресс и подумаем о практических шагах, которые могут помочь тебе справиться с этими чувствами.';
  } 
  
  if (lowerMessage.includes('грусть') || lowerMessage.includes('депрессия') || lowerMessage.includes('печаль')) {
    return 'Я слышу, что ты испытываешь грусть. Эти чувства важно признавать и давать себе право на них. Расскажи подробнее о том, что происходит в твоей жизни. Вместе мы можем найти способы, которые помогут тебе двигаться вперед, шаг за шагом.';
  }
  
  if (lowerMessage.includes('учеба') || lowerMessage.includes('экзамены') || lowerMessage.includes('сессия')) {
    return 'Учебный стресс — это то, с чем сталкиваются многие студенты. Важно находить баланс между учебой и отдыхом. Какие конкретные аспекты учебы вызывают у тебя наибольшие трудности? Может быть, мы сможем разработать стратегию, которая поможет тебе справляться с ними более эффективно.';
  }
  
  if (lowerMessage.includes('отношения') || lowerMessage.includes('друзья') || lowerMessage.includes('конфликт')) {
    return 'Отношения с другими людьми могут быть источником как радости, так и стресса. Расскажи подробнее о ситуации, которая тебя беспокоит. Вместе мы можем рассмотреть разные перспективы и найти конструктивные способы взаимодействия.';
  }
  
  if (lowerMessage.includes('привет') || lowerMessage.includes('здравствуй')) {
    return 'Привет! Рад/а, что ты обратился/лась ко мне. Как ты себя чувствуешь сегодня? Есть ли что-то конкретное, о чем ты хотел/а бы поговорить?';
  }
  
  // Ответ по умолчанию
  return 'Спасибо, что поделился/лась этим со мной. Расскажи подробнее о своих чувствах в этой ситуации. Что ты испытываешь прямо сейчас?';
} 