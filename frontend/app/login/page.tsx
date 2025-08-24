"use client";
import { useState } from "react";
import Image from "next/image";
import "animate.css";
import Link from "next/link";
import { SignupPrompt } from "../components/SignupPrompt";

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="absolute font-bold text-4xl inset-0 mx-auto w-fit h-fit top-[20%] animate__animated animate__fadeInDown">
        User Login
      </h1>

      <form
        action=""
        method="post"
        className="flex flex-col gap-12 w-11/12 sm:w-2/3 md:w-1/3 p-8 rounded-lg shadow-lg"
      >

        <label htmlFor="usernameEmail" className="w-full">
          <input
            className="p-2 border-b border-gray-400 outline-none text-md font-regular bg-transparent w-full"
            placeholder="Username or Email"
            type="text"
            id="usernameEmail"
            name="usernameEmail"
            autoFocus
            required
          />
        </label>


        <label htmlFor="password" className="relative w-full">
         <input
            className="p-2 border-b border-gray-400 outline-none text-md font-regular bg-transparent w-full pr-12"
            placeholder="Password (8-32 characters)"
            type={showPassword ? "text" : "password"}
            id="password"
            name="password"
            required
            minLength={8}
            maxLength={32}
            pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,32}$"
            title="Password must be 8-32 characters, include letters and numbers."
            />
          <button
            type="button"
            onClick={() => setShowPassword((prev) => !prev)}
            className="absolute right-2 top-2"
          >
            {showPassword ? (
              <Image
                src="/eye-open.svg"
                alt="Hide Password"
                width={20}
                height={20}
              />
            ) : (
              <Image
                src="/eye-closed.svg"
                alt="Show Password"
                width={20}
                height={20}
              />
            )}
          </button>
        </label>


        <button
          type="submit"
          className="cursor-pointer p-3 font-bold bg-gray-600 text-white rounded-md hover:bg-gray-800 transition"
        >
          Submit
        </button>
      </form>
      <SignupPrompt mode="login"/>
    </main>
  );
};

export default Login;
