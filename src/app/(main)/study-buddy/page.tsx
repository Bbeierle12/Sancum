'use client';

import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { BrainCircuit, LoaderCircle, Sparkles, AlertTriangle } from 'lucide-react';
import { getStudyBuddyResponse } from '@/lib/actions';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const initialState = {
  answer: null,
  error: null,
};

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending} className="w-full sm:w-auto">
      {pending ? (
        <>
          <LoaderCircle className="animate-spin" />
          Thinking...
        </>
      ) : (
        <>
          <BrainCircuit />
          Ask Study Buddy
        </>
      )}
    </Button>
  );
}

export default function StudyBuddyPage() {
  const [state, formAction] = useActionState(getStudyBuddyResponse, initialState);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Scripture Study Buddy</h1>
        <p className="text-lg text-muted-foreground">
          Ask questions and gain deeper insights into the scriptures.
        </p>
      </div>

      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="font-headline">Ask a Question</CardTitle>
          <CardDescription>
            Enter a scripture reference and your question to start a conversation with your AI study buddy.
          </CardDescription>
        </CardHeader>
        <form action={formAction}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="scripture">Scripture Reference</Label>
              <Input id="scripture" name="scripture" placeholder="e.g., John 3:16" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="question">Your Question</Label>
              <Textarea
                id="question"
                name="question"
                placeholder="e.g., What does it mean to be 'born again'?"
                className="min-h-[150px]"
                required
              />
            </div>
          </CardContent>
          <CardFooter>
            <SubmitButton />
          </CardFooter>
        </form>
      </Card>

      {state.error && (
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="font-headline">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertTitle>An error occurred</AlertTitle>
              <AlertDescription>{state.error}</AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}

      {state.answer && (
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="font-headline flex items-center gap-2">
              <Sparkles className="text-primary" />
              Study Buddy's Response
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 border-l-4 border-primary bg-primary/10 rounded-r-md">
              <h3 className="font-bold text-lg font-headline">{state.answer.verse.reference}</h3>
              <blockquote className="mt-2 pl-4 border-l-2 border-primary/50 text-base italic">
                "{state.answer.verse.text}"
              </blockquote>
            </div>

            <div className="space-y-1">
              <h4 className="font-bold font-headline text-lg">Explanation</h4>
              <p className="text-muted-foreground">{state.answer.explanation}</p>
            </div>

            <div className="space-y-1">
              <h4 className="font-bold font-headline text-lg">Application</h4>
              <p className="text-muted-foreground">{state.answer.application}</p>
            </div>

            {state.answer.prayer && (
              <div className="space-y-1">
                <h4 className="font-bold font-headline text-lg">Prayer</h4>
                <p className="text-muted-foreground italic">{state.answer.prayer}</p>
              </div>
            )}

            <div>
              <h4 className="font-bold font-headline text-lg">Cross-references</h4>
              <div className="mt-2 space-y-4">
                {state.answer.cross_reference.map((cr) => (
                  <div key={cr.reference} className="pl-4 border-l-2 border-accent">
                    <p className="font-semibold">{cr.reference}</p>
                    <p className="italic text-sm text-muted-foreground">"{cr.text}"</p>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
