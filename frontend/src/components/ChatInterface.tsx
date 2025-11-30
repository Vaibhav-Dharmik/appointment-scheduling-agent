import { useEffect, useRef, useState } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Loader2, Calendar, MessageSquare } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
}

export const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const messageIdRef = useRef(0);

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! I'm your medical appointment scheduling assistant. I can help you:\n\n• Schedule appointments (General, Follow-up, Physical Exam, Specialist)\n• Answer questions about the clinic\n• Check available time slots\n• Handle rescheduling or cancellations\n\nHow can I assist you today?",
      created_at: new Date().toISOString(),
    };

    setMessages([welcomeMessage]);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);

    // Add user message to chat
    const userMessage: Message = {
      id: `user-${++messageIdRef.current}`,
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Build messages array for API
      const messagesForApi = [
        ...messages.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
        { role: "user", content: message },
      ];

      // Call backend /api/chat endpoint
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: messagesForApi }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      if (!data.reply) {
        throw new Error("No response from assistant");
      }

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: `assistant-${++messageIdRef.current}`,
        role: "assistant",
        content: data.reply,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      toast({
        title: "Error",
        description:
          error instanceof Error
            ? error.message
            : "Failed to send message. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const quickActions = [
    {
      icon: Calendar,
      label: "Schedule Appointment",
      message: "I'd like to schedule an appointment",
    },
    {
      icon: MessageSquare,
      label: "Clinic Information",
      message: "Can you tell me about the clinic hours and location?",
    },
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages
          .filter(
            (msg): msg is Message & { role: "user" | "assistant" } =>
              msg.role !== "system"
          )
          .map((msg, index) => (
            <ChatMessage
              key={msg.id || index}
              role={msg.role}
              content={msg.content}
              timestamp={new Date(msg.created_at).toLocaleTimeString()}
            />
          ))}

        {isLoading && (
          <div className="flex gap-3 p-4">
            <div className="w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center shadow-soft">
              <Loader2 className="w-4 h-4 text-primary-foreground animate-spin" />
            </div>
            <div className="flex-1">
              <p className="text-sm text-muted-foreground">
                Assistant is typing...
              </p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick actions - shown when no messages yet */}
      {messages.length <= 1 && (
        <div className="px-6 pb-4">
          <div className="flex gap-3 flex-wrap">
            {quickActions.map((action) => (
              <Button
                key={action.label}
                variant="outline"
                size="sm"
                onClick={() => handleSendMessage(action.message)}
                disabled={isLoading}
                className="gap-2 hover:shadow-soft transition-smooth"
              >
                <action.icon className="h-4 w-4" />
                {action.label}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Input area */}
      <div className="border-t bg-card p-6">
        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder="Ask about appointments, clinic info, or anything else..."
        />
      </div>
    </div>
  );
};
