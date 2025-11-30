import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export const ChatMessage = ({ role, content, timestamp }: ChatMessageProps) => {
  const isAssistant = role === "assistant";

  return (
    <div
      className={cn(
        "flex gap-3 p-4 rounded-lg animate-in slide-in-from-bottom-2 duration-300",
        isAssistant ? "bg-card" : "bg-secondary/50 ml-auto max-w-[80%]"
      )}
    >
      {isAssistant && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center shadow-soft">
          <Bot className="w-4 h-4 text-primary-foreground" />
        </div>
      )}

      <div className="flex-1 space-y-1">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-foreground">
            {isAssistant ? "Medical Assistant" : "You"}
          </span>
          {timestamp && (
            <span className="text-xs text-muted-foreground">{timestamp}</span>
          )}
        </div>
        <p className="text-sm text-foreground leading-relaxed whitespace-pre-wrap">
          {content}
        </p>
      </div>

      {!isAssistant && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center shadow-soft">
          <User className="w-4 h-4 text-accent-foreground" />
        </div>
      )}
    </div>
  );
};
