"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

type Props = {};

const page = (props: Props) => {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState({
    id: "",
    email: "",
    is_active: null,
  });

  useEffect(() => {
    const getUserInfo = async () => {
      const response = await fetch("http://localhost:8000/users/me", {
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data);
        setIsAuthenticated(true);
      } else {
        console.error("Error:", response.status, response.statusText);
        router.push("/login");
      }
    };
    getUserInfo();
  }, []);

  return (
    isAuthenticated && (
      <div>
        <Link href="/login">Login</Link>
        <div>id: {user.id}</div>
        <div>email: {user.email}</div>
        <div>is_active: {user.is_active}</div>
      </div>
    )
  );
};

export default page;
