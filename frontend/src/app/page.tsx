
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Feather, BookOpen, Brain, Users } from 'lucide-react';

const features = [
  {
    icon: <BookOpen className="h-8 w-8 text-primary" />,
    title: 'Verse Display & Notes',
    description: 'Focus on the scripture that matters to you, with your personal notes and tags right alongside.',
  },
  {
    icon: <Brain className="h-8 w-8 text-primary" />,
    title: 'Spaced Repetition',
    description: 'Commit verses to heart with our intelligent SM-2 based review system that adapts to your memory.',
  },
  {
    icon: <Feather className="h-8 w-8 text-primary" />,
    title: 'Fulfillment Journal',
    description: 'Record your spiritual experiences and connect them to the covenants you are striving to keep.',
  },
  {
    icon: <Users className="h-8 w-8 text-primary" />,
    title: 'Group Sharing',
    description: 'Create or join groups to share insights and encouragement on your spiritual journey.',
  },
];

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background font-body">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <div className="mr-4 flex items-center">
            <Feather className="h-6 w-6 text-primary mr-2" />
            <span className="font-bold font-headline text-lg">Sanctum</span>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-2">
            <Button asChild variant="ghost">
                <Link href="/auth">Sign In</Link>
            </Button>
            <Button asChild>
                <Link href="/auth">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <section className="py-20 md:py-32">
          <div className="container text-center">
            <h1 className="text-4xl font-extrabold tracking-tight font-headline lg:text-6xl">
              A Sacred Space for Scripture Study
            </h1>
            <p className="mt-6 max-w-2xl mx-auto text-lg text-muted-foreground">
              Sanctum helps you deepen your connection with the word through focused tools for memorization, reflection, and journaling.
            </p>
            <div className="mt-8 flex justify-center gap-4">
              <Button asChild size="lg">
                <Link href="/auth">Start Your Journey</Link>
              </Button>
            </div>
          </div>
        </section>

        <section id="features" className="py-20 bg-secondary/50">
          <div className="container">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold font-headline">Features Designed for Deeper Study</h2>
              <p className="mt-4 text-muted-foreground">Tools to illuminate your path and anchor your understanding.</p>
            </div>
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
              {features.map((feature) => (
                <Card key={feature.title} className="text-center shadow-lg">
                  <CardHeader>
                    <div className="mx-auto bg-primary/10 p-4 rounded-full w-fit">
                        {feature.icon}
                    </div>
                    <CardTitle className="font-headline pt-4">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
        
        <section className="py-20 md:py-32">
            <div className="container text-center">
                <h2 className="text-3xl font-bold font-headline">Ready to Begin?</h2>
                <p className="mt-4 max-w-xl mx-auto text-muted-foreground">Create your free account and start building your personal sanctum for scripture study today.</p>
                <div className="mt-8">
                     <Button asChild size="lg">
                        <Link href="/auth">Create Account</Link>
                    </Button>
                </div>
            </div>
        </section>
      </main>
      
      <footer className="py-6 md:px-8 md:py-0 border-t">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
            <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                Built by Sanctum. The source code is available on GitHub.
            </p>
        </div>
      </footer>
    </div>
  );
}
