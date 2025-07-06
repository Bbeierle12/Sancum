'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';

type VerseCardProps = {
  reference: string;
  text: string;
  tags: string[];
};

export function VerseCard({ reference, text, tags }: VerseCardProps) {
  const { toast } = useToast();

  const handleReview = (quality: string) => {
    toast({
      title: 'Review Recorded',
      description: `You rated "${reference}" as "${quality}".`,
    });
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-lg">
      <CardHeader>
        <CardTitle className="font-headline text-3xl">{reference}</CardTitle>
        <CardDescription>From your scheduled review</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-lg leading-relaxed">{text}</p>
        <Separator className="my-4" />
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <Badge key={tag} variant="secondary">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="flex flex-col sm:flex-row justify-between items-center gap-4">
        <p className="text-sm text-muted-foreground">How well did you recall this verse?</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 w-full sm:w-auto">
          <Button variant="outline" onClick={() => handleReview('Again')}>
            Again
          </Button>
          <Button variant="outline" onClick={() => handleReview('Hard')}>
            Hard
          </Button>
          <Button variant="outline" onClick={() => handleReview('Good')}>
            Good
          </Button>
          <Button variant="default" onClick={() => handleReview('Easy')}>
            Easy
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}