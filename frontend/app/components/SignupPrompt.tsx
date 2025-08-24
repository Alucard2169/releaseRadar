import Link from "next/link";

interface SignupPromptProps {
  mode: "login" | "register";
}

export const SignupPrompt: React.FC<SignupPromptProps> = ({ mode }) => {
  return mode === "login" ? (
    <p className="text-white text-sm">
      New User?{" "}
      <Link
        href="/register"
        className="text-black bg-blue-500 p-1 rounded-md font-bold"
      >
        Register
      </Link>
    </p>
  ) : (
    <p className="text-white text-sm">
      Already a User?{" "}
      <Link
        href="/login"
        className="text-black bg-blue-500 p-1 rounded-md font-bold"
      >
        Login
      </Link>
    </p>
  );
};
