"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useState } from "react";

type Props = {};

const page = (props: Props) => {
  const router = useRouter();

  // States
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const validateFormData = () => {
    if (formData.username === "") {
      alert("Username is required");
      return false;
    }
    if (formData.email === "") {
      alert("Email is required");
      return false;
    }
    if (formData.password === "") {
      alert("Password is required");
      return false;
    }
    if (formData.passwordConfirm === "") {
      alert("Password confirmation is required");
      return false;
    }
    if (formData.password !== formData.passwordConfirm) {
      alert("Passwords do not match");
      return false;
    }
    return true;
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!validateFormData()) {
      return;
    }
    validateFormData();

    // Submit the form data to the specified URL
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        credentials: "include",
      });

      // Handle response here
      if (response.ok) {
        // The request was successful
        const data = await response.json();
        router.push("/dashboard");
      } else {
        // The request failed, redirect to /login
        console.error("Error:", response.status, response.statusText);
      }
    } catch (error) {
      // Handle network errors
      console.error("Network error:", error);
    }
  };

  return (
    <div className="grid h-screen place-content-center">
      <div className="rounded bg-slate-50 p-3 shadow">
        <div className="flex flex-col items-center justify-center">
          <div className="w-96">
            <h1 className="mb-4 text-4xl font-bold">Login</h1>

            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="username" className="sr-only">
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  id="username"
                  placeholder="Username"
                  className="w-full rounded-lg border-2 bg-slate-100 p-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={formData.username}
                  onChange={(e) =>
                    setFormData({ ...formData, username: e.target.value })
                  }
                />
              </div>
              <div className="mb-4">
                <label htmlFor="email" className="sr-only">
                  Username
                </label>
                <input
                  type="email"
                  name="email"
                  id="email"
                  placeholder="Email"
                  className="w-full rounded-lg border-2 bg-slate-100 p-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>
              <div className="mb-4">
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  id="password"
                  placeholder="Password"
                  className="w-full rounded-lg border-2 bg-slate-100 p-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                />
              </div>
              <div className="mb-4">
                <label htmlFor="password" className="sr-only">
                  Confirm Password
                </label>
                <input
                  type="password"
                  name="password-confirm"
                  id="password-confirm"
                  placeholder="Confirm Password"
                  className="w-full rounded-lg border-2 bg-slate-100 p-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={formData.passwordConfirm}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      passwordConfirm: e.target.value,
                    })
                  }
                />
              </div>
              <div className="mb-4">
                <button
                  type="submit"
                  className="w-full rounded-lg bg-blue-500 px-4 py-3 font-medium text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
                >
                  Login
                </button>
              </div>
            </form>
            <Link href="/dashboard">Dashboard</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default page;
