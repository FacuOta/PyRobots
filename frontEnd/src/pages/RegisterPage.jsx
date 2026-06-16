import Register from '../components/Register';
import styles from './RegisterPage.module.css'

const RegisterPage = () => {
  return (
    <div>
      <Register />
      <p className = {styles.rules}>La contraseña debe contener al menos una mayúscula</p>
      <p className = {styles.rules}>La contraseña debe contener al menos una minúscula</p>
      <p className = {styles.rules}>La contraseña debe contener al menos 8 caracteres</p>
      <p className = {styles.rules}>La contraseña debe contener al menos un número</p>
    </div>
  );
}

export default RegisterPage;
