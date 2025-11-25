export interface User {
  name: string,
  password: string,
  email: string
}

export interface authResponse {
  token_type: string;
  access_token: string;
}
