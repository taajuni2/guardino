interface EventItem {
  id: string;
  title: string;
  severity: 'info' | 'critical' | 'warning';
  agent: string;
  agentName: string;
  description?: string;
  timestamp: string;
  meta?: string;
}
