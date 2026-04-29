
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { motion, useReducedMotion } from "framer-motion";
import { Chrome, Github, Twitter } from "lucide-react";

import { useAuth } from '../contexts/AuthContext';
import { FaYandexInternational, FaDiscord, FaSoundcloud, FaGoogle } from "react-icons/fa";


const socialProviders = [
    { name: "Google", icon: FaGoogle, id: "yandex" },
    { name: "Discord", icon: FaDiscord, id: "discord" },
    { name: "Yandex", icon: FaYandexInternational, id: "yandex" },
    //   { name: "Soundcloud", icon: FaSoundcloud },
];

export function Login() {
    const shouldReduceMotion = useReducedMotion();
    const { user, isLoading, login, logout } = useAuth();
    const handleSubmit = (event) => {
        event.preventDefault();
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
                duration: 0.45,
                ease: shouldReduceMotion ? "linear" : [0.16, 1, 0.3, 1],
            }}
            className="group w-full max-w-lg rounded-3xl overflow-hidden border border-border/60 bg-card/85 p-8 backdrop-blur-xl sm:p-10 relative mx-auto"
            role="form"
            aria-labelledby="glass-sign-in-title"
        >
            <div
                aria-hidden="true"
                className="absolute inset-0 bg-gradient-to-br from-foreground/[0.04] via-transparent to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100 -z-10"
            />
            <div className="mb-8 space-y-2 text-center">
                <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-border/60 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.28em] text-muted-foreground">
                    Sign In
                </div>
                <h1
                    id="glass-sign-in-title"
                    className="text-2xl font-semibold text-foreground sm:text-3xl"
                >
                    Access your workspace
                </h1>
                <p className="text-sm text-muted-foreground">
                    Choose a social account to sing in with.
                </p>
            </div>

            <div className="mb-8 grid gap-3 sm:grid-cols-3">
                {socialProviders.map((provider) => (
                    <Button
                        key={provider.name}
                        variant="outline"
                        onClick={() => login(provider.id)}
                        className="flex items-center justify-center gap-2 rounded-full border-border/60 bg-card/70 text-sm text-foreground transition-transform duration-300 hover:-translate-y-1 hover:text-primary"
                        aria-label={`Continue with ${provider.name}`}
                    >
                        <provider.icon className="h-4 w-4" aria-hidden />
                        <span className="hidden sm:inline">{provider.name}</span>
                    </Button>
                ))}
            </div>


            <p className="mt-6 text-center text-xs text-muted-foreground">
                By continuing you agree to our terms of service and privacy policy.
            </p>
        </motion.div>
    );
}
