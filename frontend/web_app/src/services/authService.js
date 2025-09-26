import api from '../utils/api';

// Map UI selection to backend roles
const mapUserTypeToRole = (userType) => {
  const mapping = {
    citizen: 'citizen',
    authority: 'authority',
    analyst: 'analyst',
  };
  return mapping[userType] || 'citizen';
};

export const register = async ({ email, full_name, phone, password, userType }) => {
  const payload = {
    email,
    full_name,
    phone,
    password,
    role: mapUserTypeToRole(userType),
  };
  const { data } = await api.post('/auth/register', payload);
  return data;
};

export const login = async ({ email, password }) => {
  // OAuth2PasswordRequestForm expects x-www-form-urlencoded with username=password
  const form = new URLSearchParams();
  form.append('username', email);
  form.append('password', password);
  const { data } = await api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data; // { access_token, token_type }
};


