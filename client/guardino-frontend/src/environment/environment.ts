export const environment = {
  production: false,
  apiUrl: 'http://192.168.110.60:8000', // muss auf backend adresse der VM geändert werden oder localhost für lokale entwickung
  wsUrl: 'ws://localhost:5000/',
  kafkaTopicEvents: 'agent-events',
  kafkaTopicAgent: 'agent-lifecycle'
};
