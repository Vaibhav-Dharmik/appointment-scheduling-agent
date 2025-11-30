import { ChatInterface } from "@/components/ChatInterface";
import { Card } from "@/components/ui/card";
import { Activity, Calendar, Clock, Shield } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-subtle">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-soft">
                <Activity className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-foreground">MediSchedule</h1>
                <p className="text-xs text-muted-foreground">Intelligent Appointment Scheduling</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="hidden md:flex items-center gap-1 px-3 py-1.5 rounded-full bg-accent/10 text-accent text-sm font-medium">
                <Clock className="w-4 h-4" />
                <span>24/7 Available</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Info Cards */}
          <div className="grid md:grid-cols-3 gap-4 mb-8 animate-in slide-in-from-top duration-500">
            <Card className="p-4 bg-card hover:shadow-medium transition-smooth">
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Calendar className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm text-foreground mb-1">Smart Scheduling</h3>
                  <p className="text-xs text-muted-foreground">
                    AI-powered appointment booking with real-time availability
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-4 bg-card hover:shadow-medium transition-smooth">
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-accent/10">
                  <Activity className="w-5 h-5 text-accent" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm text-foreground mb-1">Instant Answers</h3>
                  <p className="text-xs text-muted-foreground">
                    Get quick answers to clinic FAQs and policies
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-4 bg-card hover:shadow-medium transition-smooth">
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-secondary/50">
                  <Shield className="w-5 h-5 text-foreground" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm text-foreground mb-1">Secure & Private</h3>
                  <p className="text-xs text-muted-foreground">
                    Your health information is protected and confidential
                  </p>
                </div>
              </div>
            </Card>
          </div>

          {/* Chat Interface */}
          <Card className="overflow-hidden shadow-medium animate-in slide-in-from-bottom duration-700">
            <div className="h-[calc(100vh-280px)] min-h-[500px] flex flex-col">
              <ChatInterface />
            </div>
          </Card>

          {/* Footer Info */}
          <div className="mt-6 text-center animate-in fade-in duration-1000">
            <p className="text-sm text-muted-foreground">
              Clinic Hours: Mon-Fri 8:00 AM - 6:00 PM, Sat 9:00 AM - 2:00 PM
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              Emergency? Call 911 or visit the nearest emergency room
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
