import Login from '../components/Login';
import styles from "./LoginPage.module.css";

function LoginPage() {

  return (
    <div>
      <h1 className={styles.title}>PyRobots</h1>
      <Login />
    </div>
  );
}

export default LoginPage;
